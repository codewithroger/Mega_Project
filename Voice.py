import os
from pydub import AudioSegment
import pandas as pd

# Ensure you have the required libraries installed:
# pip install pydub pandas

def split_audio(input_file, frames_output_dir, csv_output_dir, frame_duration=5000):
    """
    Split the audio into frames and save each frame as a .wav file.

    Parameters:
    - input_file: Path to the input .wav file.
    - frames_output_dir: Directory to save the frames.
    - csv_output_dir: Directory to save the CSV files.
    - frame_duration: Duration of each frame in milliseconds (default is 5000 ms or 5 seconds).
    """
    # Ensure input file exists
    if not os.path.exists(input_file):
        print(f"Error: The input file '{input_file}' does not exist.")
        return
    
    # Ensure the input file is a .wav file
    if not input_file.lower().endswith('.wav'):
        print(f"Error: The input file '{input_file}' is not a .wav file.")
        return

    # Load the audio file
    try:
        audio = AudioSegment.from_wav(input_file)
    except Exception as e:
        print(f"Error loading the audio file: {e}")
        return

    total_duration = len(audio)
    frame_count = 0
    
    # Ensure output directories exist
    os.makedirs(frames_output_dir, exist_ok=True)
    os.makedirs(csv_output_dir, exist_ok=True)
    
    # List to store new CSV information
    new_csv_data = []
    
    # Get base name of the input file to use in naming
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # Iterate through the audio, slicing out 5-second frames
    for start in range(0, total_duration, frame_duration):
        end = min(start + frame_duration, total_duration)
        frame = audio[start:end]
        frame_name = f"{base_name}_frame_{frame_count}.wav"
        frame_path = os.path.join(frames_output_dir, frame_name)
        
        # Export the frame
        frame.export(frame_path, format="wav")
        
        # Append data for new CSV entries with label "Yogesh"
        new_csv_data.append({
            "frame_name": frame_name,
            "fsID": frame_count,
            "start": start / 1000.0,  # Convert to seconds
            "end": end / 1000.0,      # Convert to seconds
            "salience": 1,            # Default salience, can be adjusted based on the use case
            "fold": 3,                # Default fold value, can be adjusted
             "classId": 2,             # Default class ID, can be adjusted
            "Label": "Sushan"
        })
        
        frame_count += 1
    
    # Define CSV file path
    csv_output_path = os.path.join(csv_output_dir, "frames_metadata.csv")
    
    # If the CSV file already exists, append to it; otherwise, create a new one
    if os.path.exists(csv_output_path):
        # Read the existing data
        existing_df = pd.read_csv(csv_output_path)
        
        # Check for duplicates based on frame_name
        new_df = pd.DataFrame(new_csv_data)
        combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset='frame_name', keep='first')
        
        # Save back to CSV
        combined_df.to_csv(csv_output_path, index=False)
    else:
        # If CSV does not exist, create it
        new_df = pd.DataFrame(new_csv_data)
        new_df.to_csv(csv_output_path, index=False)
    
    print(f"Frames saved to {frames_output_dir} and metadata CSV updated at {csv_output_path}.")

# Example usage
input_wav_file = "C:/Users/yoges/Downloads/sushan.wav"  # Replace with your input .wav file path
frames_directory = "D:/MegaProject/venv/Voice/fold3"  # Directory to save frames
csv_directory = "D:/MegaProject/venv/Voice"  # Directory to save CSV files

split_audio(input_wav_file, frames_directory, csv_directory)
