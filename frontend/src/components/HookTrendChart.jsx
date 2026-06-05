import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";

export default function HookTrendChart({ videos }) {

  const chartData = videos.map((video, index) => ({
    name: video.title.substring(0, 15),
    hook_score: video.hook_score || 0
  }));

  return (
    <div
      className="
        bg-white
        rounded-xl
        shadow-md
        p-6
        mb-8
      "
    >
      <h2
        className="
          text-xl
          font-semibold
          mb-4
        "
      >
        Hook Score Trend
      </h2>

      <ResponsiveContainer
        width="100%"
        height={300}
      >
        <LineChart data={chartData}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="name" />

          <YAxis domain={[0, 100]} />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="hook_score"
            stroke="#2563eb"
            strokeWidth={3}
          />

        </LineChart>
      </ResponsiveContainer>

    </div>
  );
}