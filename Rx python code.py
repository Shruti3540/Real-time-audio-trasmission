import serial
import pyaudio
import time
import numpy as np
 
def receive_and_play_uart(port="COM5", baudrate=115200, chunk_size=5500, timeout=10):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt8,  # PyAudio expects signed
            channels=1,
            rate=1920, 
            output=True
        )

        print("Receiving raw PCM bytes (unsigned), converting to signed, and playing...")

        last_received = time.time()

        while True:
            data = ser.read(chunk_size)
            if data:
                last_received = time.time()

                # Convert unsigned bytes (0–255) to signed (-128 to 127)
                pcm_signed = bytes(np.frombuffer(data, dtype=np.uint8).astype(np.int8))

                stream.write(pcm_signed)
                print(f"Played {len(data)} bytes")

            else:
                if time.time() - last_received > timeout:
                    print("No data received. Timeout.")
                    break

    except KeyboardInterrupt:
        print("Stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            stream.stop_stream()
            stream.close()
            p.terminate()
            ser.close()
        except:
            pass

if _name_ == "_main_":
    receive_and_play_uart()