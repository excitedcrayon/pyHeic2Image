#!/usr/bin/python3

import tkinter as tk
from tkinter import filedialog, messagebox
from pillow_heif import register_heif_opener
from PIL import Image


class HEIC2Image:
    def __init__(self, master):
        self.master = master
        master.title("HEIC 2 Image")
        master.geometry("600x600")
        master.resizable(False, False)
        master.iconbitmap("logo.ico")
        self.filePaths = [] # list to store the opened multiple files

        # center the GUI
        self.centerWindow(master)
        # label
        self.renderWidgets(master)

    def centerWindow(self, master):
        screenWidth = master.winfo_screenwidth()
        screenHeight = master.winfo_screenheight()
        xCoord = (screenWidth / 2) - (600 / 2)
        yCoord = (screenHeight / 2) - (600 / 2)
        master.geometry("+%d+%d" % (xCoord, yCoord))

    def renderWidgets(self, master):
        # Frame to hold label and scrollbar
        frame = tk.Frame(master)
        frame.grid(
            row=0,
            column=0,
            rowspan=1,
            columnspan=6,
            sticky="nsew"
        )

        # label with scrollbar
        self.textScrollBar = tk.Scrollbar(
            frame,
            orient="vertical"
        )
        self.textScrollBar.pack(
            side="right",
            fill="y"
        )
        self.label = tk.Text(
            frame,
            bg="white",
            wrap="word",
            yscrollcommand=self.textScrollBar.set
        )
        self.label.pack(
            side="left",
            fill="both",
            expand=True
        )
        self.textScrollBar.config(command=self.label.yview)

        # open button
        self.openImageFilesButton = tk.Button(
            master,
            text="Open HEIC Images",
            command=lambda: self.openHeicImages(self.label)
        )
        self.openImageFilesButton.grid(
            row=1,
            column=1,
            sticky="ew"
        )
        # convert to JPG button
        self.convertToJPGButton = tk.Button(
            master,
            text="Convert To JPG",
            command=lambda: self.convertToJPG(self.label)
        )
        self.convertToJPGButton.grid(
            row=1,
            column=2,
            sticky="ew"
        )
        # convert to PNG button
        self.convertToPNGButton = tk.Button(
            master,
            text="Convert To PNG",
            command=lambda: self.convertToPNG(self.label)
        )
        self.convertToPNGButton.grid(
            row=1,
            column=3,
            sticky="ew"
        )
        # clear list button
        self.clearListButton = tk.Button(
            master,
            text="Clear List",
            command=lambda: self.clearFileList(self.label)
        )
        self.clearListButton.grid(
            row=1,
            column=4,
            sticky="ew"
        )
        # close button
        self.closeButton = tk.Button(
            master,
            text="Close",
            command=lambda: self.closeWindow(master)
        )
        self.closeButton.grid(
            row=1,
            column=5,
            sticky="ew"
        )

        # Configure buttons to have same size and fill in row 2
        for col in range(1, 6):
            master.grid_columnconfigure(col, weight=1, uniform="buttons")        

        # configure grid weights to make label expandable
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

    def openHeicImages(self, label):
        self.filePaths = filedialog.askopenfilenames(
            filetypes=[("HEIC files", "*.heic")]
        )
        if self.filePaths:
            for file in self.filePaths:
                filename = file.split("/")[-1] # extract file name from path
                label.insert(tk.END, filename + "\n")

    def convertToJPG(self, label):
        saveDirectory = filedialog.askdirectory(
            title="Choose directory to save JPG image(s)"
        )      
        if saveDirectory:
            if self.filePaths:
                label.insert(tk.END, "JPG Conversion initiated...\n")
                for file in self.filePaths:
                    # open HEIC image
                    register_heif_opener()
                    heicImage = Image.open(file)

                    # convert to JPG
                    jpgImage = saveDirectory + "/" + file.rsplit('/', 1)[-1].rsplit('.', 1)[0] + ".jpg"
                    heicImage.convert('RGB').save(jpgImage, format="JPEG")                

                    #update label to show converted files
                    updatedFile = jpgImage.split("/")[-1]
                    label.insert(tk.END, "Converted file: " + updatedFile + " saved\n")
                self.getFileCountAndImageType(self.filePaths, 'jpg')
                self.cleanUpFileListOnSave(label)
        else:
            label.insert(tk.END, "No HEIC files opened\nSave location not selected\nSkipping conversion...\n")
            pass       

    def convertToPNG(self, label):
        saveDirectory = filedialog.askdirectory(
            title="Choose directory to save PNG image(s)"
        )      
        if saveDirectory:
            if self.filePaths:
                label.insert(tk.END, "PNG Conversion initiated...\n")
                for file in self.filePaths:
                    # open HEIC image
                    register_heif_opener()
                    heicImage = Image.open(file)

                    # convert to PNG
                    pngImage = saveDirectory + "/" + file.rsplit('/', 1)[-1].rsplit('.', 1)[0] + ".png"
                    heicImage.convert('RGB').save(pngImage, format="PNG")

                    #update label to show converted files
                    updatedFile = pngImage.split("/")[-1]
                    label.insert(tk.END, updatedFile + "\n")
                self.getFileCountAndImageType(self.filePaths, 'png')
                self.cleanUpFileListOnSave(label)
        else:
            label.insert(tk.END, "No HEIC files opened\nSave location not selected\nSkipping conversion...\n")
            pass     

    def cleanUpFileListOnSave(self, label):
        self.filePaths = []
        label.insert(tk.END, "Cleaning up previously selected files...\nSelect new files to convert or close the program")

    def getFileCountAndImageType(self, list, imageType):
        messagebox.showinfo(
            "Conversion Complete",
            str(len(list)) + " images have been converted to " + imageType
        )

    def clearFileList(self, label):
        if len(self.filePaths) > 0:
            self.filePaths = []
            label.delete("1.0",tk.END)
            messagebox.showinfo(
                "Info",
                "HEIC Images list cleared"
            )
        else:
            messagebox.showinfo(
                "Info",
                "No image data to clear"
            )

    def closeWindow(self, master):
        if len(self.filePaths) > 0:
            result = messagebox.askquestion(
               "Shutdown",
               "You still have some files to process \nAre you sure you want to quit?"
            )

            if result == "yes":
                master.destroy()
            else:
                pass
        else:
            messagebox.showinfo(
                "Shutdown",
                "Thank you for using HEIC2Image"
            )
            master.destroy()
    
def main():
    root = tk.Tk()
    app = HEIC2Image(root)
    root.mainloop()

if __name__ == "__main__":
    main()