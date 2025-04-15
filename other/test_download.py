from program_downloader import ProgramDownloader

if __name__ == "__main__":
    print("🔧 Starting manual test of ProgramDownloader...")
    pd = ProgramDownloader()
    pd.download_programs(["Amvrosia Service"])
    print("✅ Test completed.")
