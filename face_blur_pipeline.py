import cv2
import numpy as np
import torch
from facenet_pytorch import MTCNN
from tqdm.notebook import tqdm
import base64
from IPython.display import HTML, Video
from PIL import Image

class FaceBlurPipeline:
    def __init__(self,
                input_path, output_path,
                batch_size=16, blur_ksize=(99, 99),
                blur_sigma=30):
        """
        Initializes the face blurring pipeline.

        Parameters:
            input_path (str): Path to the input video file.
            output_path (str): Path where the output video will be saved.
            batch_size (int): Number of frames to process in a batch.
            blur_ksize (tuple): Kernel size for Gaussian blur.
            blur_sigma (int): Standard deviation for Gaussian blur.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.batch_size = batch_size
        self.blur_ksize = blur_ksize
        self.blur_sigma = blur_sigma

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")

        self.mtcnn = MTCNN(keep_all=True, device=self.device)

        self.cap = cv2.VideoCapture(self.input_path)
        if not self.cap.isOpened():
            raise IOError("Error opening video file: " + self.input_path)

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.width  = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Initialize the video writer with the same resolution as original
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (self.width, self.height))

    def blur_face(self, frame, box):
        """
        Applies a Gaussian blur to the region of the frame defined by the bounding box.
        """
        x1, y1, x2, y2 = [int(b) for b in box]
        # Ensure coordinates are within frame dimensions
        x1 = max(x1, 0)
        y1 = max(y1, 0)
        x2 = min(x2, frame.shape[1])
        y2 = min(y2, frame.shape[0])

        # Extract ROI and apply Gaussian blur
        face = frame[y1:y2, x1:x2]
        face_blurred = cv2.GaussianBlur(face, self.blur_ksize, self.blur_sigma)
        frame[y1:y2, x1:x2] = face_blurred
        return frame

    def process_video(self):
        """
        Processes the video to detect and blur faces using batch processing.
        Writes the processed frames to the output video file.
        """
        frames_batch = []
        orig_frames_batch = []
        # For notebooks, tqdm.notebook is ideal; if running as a script you can use tqdm.tqdm instead.
        pbar = tqdm(total=self.frame_count, desc='Processing Frames')

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # Convert frame to RGB for detection and keep original for processing
            frames_batch.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            orig_frames_batch.append(frame)

            # Process the batch when it's full
            if len(frames_batch) == self.batch_size:
                self._process_batch(frames_batch, orig_frames_batch, pbar)
                frames_batch = []
                orig_frames_batch = []

        # Process any remaining frames
        if len(frames_batch) > 0:
            self._process_batch(frames_batch, orig_frames_batch, pbar)

        pbar.close()
        self.cap.release()
        self.out.release()
        print("Processing complete. Output saved to:", self.output_path)

    def _process_batch(self, frames_batch, orig_frames_batch, pbar):
        """
        Helper function to process a batch of frames.
        """
        # Convert the batch of frames (RGB) to PIL images for MTCNN
        pil_batch = [Image.fromarray(frame) for frame in frames_batch]
        boxes_batch, _ = self.mtcnn.detect(pil_batch)

        # Process each frame in the batch
        for idx, boxes in enumerate(boxes_batch):
            if boxes is not None:
                for box in boxes:
                    orig_frames_batch[idx] = self.blur_face(orig_frames_batch[idx], box)
            self.out.write(orig_frames_batch[idx])
            pbar.update(1)

    @staticmethod
    def display_video(video_path, width=640, height=480):
        """
        Displays a video in the notebook by embedding it in HTML.
        """
        try:
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
            video_base64 = base64.b64encode(video_bytes).decode('utf-8')
            html_code = f"""
            <video width="{width}" height="{height}" controls>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            """
            return HTML(html_code)
        except Exception as e:
            return f"Error displaying video: {e}"

    @staticmethod
    def display_video_ipython(video_path, width=640, height=480):
        """
        Displays a video using IPython's Video widget.
        """
        return Video(video_path, width=width, height=height)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Process a video to blur faces.")
    parser.add_argument('--input', type=str, required=True, help="Path to the input video.")
    parser.add_argument('--output', type=str, required=True, help="Path to save the output video.")
    parser.add_argument('--batch_size', type=int, default=16, help="Batch size for processing frames.")
    args = parser.parse_args()

    pipeline = FaceBlurPipeline(input_path=args.input, output_path=args.output, batch_size=args.batch_size)
    pipeline.process_video()
