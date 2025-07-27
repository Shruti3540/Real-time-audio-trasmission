import subprocess
import os

input_mp3_path = "D://SUMMER PROJECT/Apt.mp3"             # Your MP3 input file
temp_pcm_path = "D://SUMMER PROJECT/Apt.pcm"        # Temporary PCM output (will be kept)
output_header_path = "D://SUMMER PROJECT/Apt.h"      # Final C header file
pcm_variable_name = "audio_data"         # C array name
sample_rate = 1920                       # Hz
bit_format = "s8"                        # 8-bit signed PCM
channels = 1                             # Mono

def mp3_to_pcm(mp3_path, pcm_path):
    command = [
        'ffmpeg',
        '-y',
        '-i', mp3_path,
        '-f', bit_format,
        '-ar', str(sample_rate),
        '-ac', str(channels),
        pcm_path
    ]
    subprocess.run(command, check=True)

def pcm_to_header(pcm_path, header_path, var_name="audio_data"):
    with open(pcm_path, "rb") as pcm_file:
        pcm_bytes = pcm_file.read()

    with open(header_path, "w") as header_file:
        header_file.write("#ifndef AUDIO_DATA_H\n#define AUDIO_DATA_H\n\n")
        header_file.write(f"const unsigned char {var_name}[] = {{\n    ")

        for i, byte in enumerate(pcm_bytes):
            header_file.write(f"0x{byte & 0xFF:02X}")
            if i != len(pcm_bytes) - 1:
                header_file.write(", ")
            if (i + 1) % 12 == 0:
                header_file.write("\n    ")

        header_file.write("\n};\n")
        header_file.write(f"const unsigned int {var_name}_len = {len(pcm_bytes)};\n")
        header_file.write("#endif // AUDIO_DATA_H\n")

def convert_mp3_to_header():
    mp3_to_pcm(input_mp3_path, temp_pcm_path)
    pcm_to_header(temp_pcm_path, output_header_path, pcm_variable_name)
    print(f"Header file '{output_header_path}' generated.")
    print(f"Raw PCM data saved as '{temp_pcm_path}'.")

convert_mp3_to_header()
