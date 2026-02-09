"""
Quick setup script for first-time installation
"""
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Running: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode != 0:
        print(f"\n❌ Failed: {description}")
        return False
    else:
        print(f"\n✅ Success: {description}")
        return True

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║  Sri Lanka News Scraper - Setup Script              ║
    ║  This will download required NLP models              ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Download spaCy model
    if not run_command(
        f"{sys.executable} -m spacy download en_core_web_sm",
        "Downloading spaCy English model (~50MB)"
    ):
        print("\n⚠️  Warning: spaCy model download failed.")
        print("You can manually install later with:")
        print("  python -m spacy download en_core_web_sm\n")
    
    print("\n" + "="*60)
    print("✅ Setup complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run the scraper:")
    print("   python main.py --all")
    print("\n2. Or see all options:")
    print("   python main.py --help")
    print("\nNote: Sentence-Transformer models will download")
    print("automatically (~400MB) on first use.")

if __name__ == "__main__":
    main()
