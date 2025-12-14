import fitz  # PyMuPDF
import qrcode
import os
import tkinter as tk
from tkinter import filedialog

class PDFManager:
    def __init__(self):
        # --- CONFIGURATION: ADJUST THESE TO MATCH YOUR TEMPLATE ---
        self.TEMPLATE_FILE = "LOCKSEC.pdf"
        
        # 1. USERNAME LOCATION
        self.USER_X = 35 
        self.USER_Y = 120   
        
        # 2. RESCUE KEY LOCATION
        self.KEY_X = 130   
        self.KEY_Y = 437
        self.KEY_SIZE = 24 
        
        # 3. QR CODE LOCATION
        self.QR_RECT = fitz.Rect(428, 381, 518, 471) 

    def create_recovery_kit(self, username, rescue_code, totp_uri):
        if not os.path.exists(self.TEMPLATE_FILE):
            print(f"❌ Error: {self.TEMPLATE_FILE} not found!")
            return None

        # --- OPEN SAVE DIALOG ---
        print("⏳ Waiting for user to select save location...")
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        file_path = filedialog.asksaveasfilename(
            title="Save Your LockSec Recovery Kit",
            initialfile=f"{username}_Recovery_Kit.pdf",
            defaultextension=".pdf",
            filetypes=[("PDF Documents", "*.pdf")]
        )
        
        if not file_path:
            print("❌ Save cancelled by user.")
            return None

        # --- GENERATE PDF ---
        try:
            doc = fitz.open(self.TEMPLATE_FILE)
            page = doc[0] 

            # A. Insert Username (UPDATED STYLE)
            # Color #032e76 is R=3, G=46, B=118. We divide by 255 for PDF.
            locksec_blue = (3/255, 46/255, 118/255)
            greeting="Welcome " + username + ","
            page.insert_text(
                (self.USER_X, self.USER_Y), 
                greeting, 
                fontsize=19, 
                fontname="Helvetica-Bold", 
                color=locksec_blue
            )

            # B. Insert Rescue Key
            page.insert_text(
                (self.KEY_X, self.KEY_Y), 
                rescue_code, 
                fontsize=self.KEY_SIZE, 
                fontname="Courier", 
                color=(0, 0, 0)
            )

            # C. Insert QR Code
            qr_img = qrcode.make(totp_uri)
            qr_filename = "temp_qr.png"
            qr_img.save(qr_filename)
            page.insert_image(self.QR_RECT, filename=qr_filename)

            # D. Save
            doc.save(file_path)
            doc.close()
            
            if os.path.exists(qr_filename):
                os.remove(qr_filename)

            print(f"\n✅ RECOVERY KIT SAVED: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Error creating PDF: {e}")
            return None

if __name__ == "__main__":
    pm = PDFManager()
    pm.create_recovery_kit("TestUser", "A1B2-C3D4-E5F6", "otpauth://totp/LockSec:Test?secret=JBSWY3DPEHPK3PXP")