import os
import ROOT

input_dir = "Rootfiles"
covar_path = "shapes_prefit/overall_total_covar"

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Get a list of all files matching the pattern
file_list = [filename for filename in os.listdir(input_dir) if filename.startswith("fitDiagnostics") and filename.endswith(".root")]

# Loop through the files
for filename in file_list:
    file_path = os.path.join(input_dir, filename)

    # Open the ROOT file
    root_file = ROOT.TFile.Open(file_path)

    # Get the TH2D histogram
    hist = root_file.Get(covar_path)

    if hist:
        # Create output filename
        output_filename = f"cov_{os.path.splitext(filename)[0]}"

        # Save histogram as CSV
        csv_filename = os.path.join(output_dir, f"{output_filename}.csv")
        csv_file = open(csv_filename, "w")
        for ybin in range(1, hist.GetNbinsY() + 1):
            for xbin in range(1, hist.GetNbinsX() + 1):
                csv_file.write(f"{hist.GetBinContent(xbin, ybin)},")
            csv_file.write("\n")
        csv_file.close()

        # Save histogram as PDF
        pdf_filename = os.path.join(output_dir, f"{output_filename}.pdf")
        canvas = ROOT.TCanvas("canvas", "canvas")
        hist.Draw("COLZ")
        canvas.Print(pdf_filename)

        # Clean up
        root_file.Close()
    else:
        print(f"TH2D histogram not found in {file_path}")
