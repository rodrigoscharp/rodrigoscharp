// Cut the subject out of a photo with Apple's Vision framework (macOS 14+).
// Keeps only the foreground instance under the given point (normalized, top-left origin).
// Usage: swift tools/cutout.swift in.png out.png [x y]
import AppKit
import CoreImage
import Vision

let args = CommandLine.arguments
let input = URL(fileURLWithPath: args[1]), output = URL(fileURLWithPath: args[2])
let px = args.count > 4 ? Double(args[3])! : 0.4
let py = args.count > 4 ? Double(args[4])! : 0.55

let handler = VNImageRequestHandler(url: input)
let req = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([req])
guard let obs = req.results?.first else { fatalError("no foreground found") }

// pick the instance under the point
let mask = obs.instanceMask
CVPixelBufferLockBaseAddress(mask, .readOnly)
let w = CVPixelBufferGetWidth(mask), h = CVPixelBufferGetHeight(mask)
let row = CVPixelBufferGetBytesPerRow(mask)
let base = CVPixelBufferGetBaseAddress(mask)!.assumingMemoryBound(to: UInt8.self)
let label = base[Int(py * Double(h)) * row + Int(px * Double(w))]
CVPixelBufferUnlockBaseAddress(mask, .readOnly)
print("instances:", obs.allInstances.map { $0 }, "picked:", label)
let pick: IndexSet = label == 0 ? obs.allInstances : IndexSet(integer: Int(label))

let buf = try obs.generateMaskedImage(ofInstances: pick, from: handler, croppedToInstancesExtent: false)
let ci = CIImage(cvPixelBuffer: buf)
let ctx = CIContext()
try ctx.writePNGRepresentation(of: ci, to: output, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!)
print("wrote", output.path)
