import express from "express";
import multer from "multer";
import { spawn } from "child_process";

const router = express.Router();
const upload = multer({ dest: "uploads/" });


router.post("/run", upload.single("file"), (req, res) => {
  const { chunking, embeddingModel, retriever } = req.body;
  const filePath = req.file.path;

  const python = spawn("python3", [
    "backend/scripts/run_benchmark.py",
    filePath,
    chunking,
    embeddingModel,
    retriever
  ]);

  let output = "";
  python.stdout.on("data", (data) => {
    output += data.toString();
  });

  python.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  python.on("close", (code) => {
    console.log(`Python exited with code ${code}`);
    try {
      res.json(JSON.parse(output));
    } catch (err) {
      res.status(500).json({ error: "Benchmark failed" });
    }
  });
});

export default router;
