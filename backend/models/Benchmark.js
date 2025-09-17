import mongoose from "mongoose";

const benchmarkSchema = new mongoose.Schema({
  modelName: String,
  score: Number,
  createdAt: { type: Date, default: Date.now }
});

export default mongoose.model("Benchmark", benchmarkSchema);
