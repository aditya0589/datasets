import tkinter as tk
from tkinter import ttk, filedialog
from pyspark.sql import SparkSession
from pyspark.sql.functions import input_file_name
import shutil
import os
import threading

# ---------- Spark Streaming Functionality ----------
def start_stream(source_dir, source_ext, target_dir, target_ext):
    spark = SparkSession.builder \
        .appName("RealTimeFileConverter") \
        .master("local[*]") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # Monitor the directory (assuming text files here for simplicity)
    df = spark.readStream.format("text").load(source_dir)

    # Add file name column
    df_with_name = df.withColumn("file_name", input_file_name())

    def process_batch(df, batch_id):
        # Collect file names
        files = df.select("file_name").distinct().collect()

        for row in files:
            file_path = row.file_name
            if not file_path.endswith(source_ext):
                continue

            file_name = os.path.basename(file_path)
            base_name = os.path.splitext(file_name)[0]
            target_file = os.path.join(target_dir, base_name + target_ext)

            print(f"Processing {file_path} -> {target_file}")

            # Simple content copy (no transformation)
            try:
                shutil.copy(file_path, target_file)
                print(f"Copied to {target_file}")
            except Exception as e:
                print(f"Error copying file: {e}")

    query = df_with_name.writeStream \
        .foreachBatch(process_batch) \
        .start()

    query.awaitTermination()

# ---------- Tkinter GUI ----------
def browse_source_dir():
    path = filedialog.askdirectory()
    source_dir_var.set(path)

def browse_target_dir():
    path = filedialog.askdirectory()
    target_dir_var.set(path)

def start_conversion():
    source_dir = source_dir_var.get()
    source_ext = source_ext_var.get()
    target_dir = target_dir_var.get()
    target_ext = target_ext_var.get()

    if not all([source_dir, source_ext, target_dir, target_ext]):
        print("Please fill in all fields.")
        return

    # Start Spark in a separate thread to avoid blocking the GUI
    threading.Thread(target=start_stream, args=(source_dir, source_ext, target_dir, target_ext), daemon=True).start()

# ---------- Main Window ----------
root = tk.Tk()
root.title("Real-Time File Converter (Spark Streaming)")
root.geometry("500x400")

# Variables
source_dir_var = tk.StringVar()
target_dir_var = tk.StringVar()
source_ext_var = tk.StringVar()
target_ext_var = tk.StringVar()

# Source Directory
ttk.Label(root, text="Source Directory:").pack(pady=(10, 0))
ttk.Entry(root, textvariable=source_dir_var, width=50).pack(pady=5)
ttk.Button(root, text="Browse", command=browse_source_dir).pack()

# Source File Type
ttk.Label(root, text="Source File Extension (e.g., .txt):").pack(pady=(10, 0))
ttk.Entry(root, textvariable=source_ext_var, width=20).pack(pady=5)

# Target Directory
ttk.Label(root, text="Target Directory:").pack(pady=(10, 0))
ttk.Entry(root, textvariable=target_dir_var, width=50).pack(pady=5)
ttk.Button(root, text="Browse", command=browse_target_dir).pack()

# Target File Type
ttk.Label(root, text="Target File Extension (e.g., .md):").pack(pady=(10, 0))
ttk.Entry(root, textvariable=target_ext_var, width=20).pack(pady=5)

# Start Button
ttk.Button(root, text="Start Conversion", command=start_conversion).pack(pady=20)

root.mainloop()
