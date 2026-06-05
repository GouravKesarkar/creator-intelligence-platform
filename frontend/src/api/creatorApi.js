import axios from "axios";

const API = axios.create({
  baseURL: "https://ubiquitous-space-happiness-g4r699vqgv7v39pgr-8000.app.github.dev/",
});

export const getAnalyses = () =>
  API.get("/analyses");

export const analyzeVideo = (youtubeUrl) =>
  API.post("/analyze", {
    youtube_url: youtubeUrl,
  });