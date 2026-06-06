import axios from "axios";

const API = axios.create({
  baseURL: "https://solid-space-fiesta-pjw9vv5rx57wh6rv-8000.app.github.dev/",
});

export const getAnalyses = () =>
  API.get("/analyses");

export const analyzeVideo = (youtubeUrl) =>
  API.post("/analyze", {
    youtube_url: youtubeUrl,
  });

export const getVideoDetails = (
  videoId
) =>
  API.get(
    `/videos/${videoId}`
  );