import { useEffect, useState } from "react";
import { getAnalyses } from "../api/creatorApi";
import StatCard from "../components/StatCard";
import HookTrendChart
  from "../components/HookTrendChart";

export default function Dashboard() {

  const [videos, setVideos] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    const response = await getAnalyses();
    setVideos(response.data);
  }

  const avgHook =
    videos.length > 0
      ? Math.round(
          videos.reduce(
            (sum, v) => sum + (v.hook_score || 0),
            0
          ) / videos.length
        )
      : 0;

  const bestHook =
    videos.length > 0
      ? Math.max(...videos.map(v => v.hook_score || 0))
      : 0;

  return (
    <div className="min-h-screen bg-slate-100">

      <div className="max-w-7xl mx-auto p-8">

        <h1 className="text-4xl font-bold mb-8">
          Creator Intelligence Dashboard
        </h1>

        {/* KPI Cards */}

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">

          <StatCard
            title="Videos"
            value={videos.length}
          />

          <StatCard
            title="Avg Hook"
            value={avgHook}
          />

          <StatCard
            title="Best Hook"
            value={bestHook}
          />

          <StatCard
            title="Analyses"
            value={videos.length}
          />

          <HookTrendChart
                videos={videos}
            />

        </div>

        {/* Recent Videos */}

        <div className="bg-white rounded-xl shadow-md p-6">

          <h2 className="text-xl font-semibold mb-4">
            Recent Videos
          </h2>

          <table className="w-full">

            <thead>
              <tr className="border-b">
                <th className="text-left py-3">
                  Title
                </th>

                <th className="text-left py-3">
                  Channel
                </th>

                <th className="text-left py-3">
                  Status
                </th>

                <th className="text-left py-3">
                  Hook Score
                </th>
              </tr>
            </thead>

            <tbody>

              {videos.map((video) => (

                <tr
                  key={video.video_id}
                  className="
                    border-b
                    hover:bg-gray-50
                    cursor-pointer
                  "
                >

                  <td className="py-3">
                    {video.title}
                  </td>

                  <td className="py-3">
                    {video.channel_name}
                  </td>

                   <td className="py-3">

                <span
                    className={`
                    px-3
                    py-1
                    rounded-full
                    text-white
                    text-sm

                    ${
                        video.status === "ANALYZED"
                        ? "bg-green-500"
                        : "bg-red-500"
                    }
                    `}
                >
                    {video.status}
                </span>

                </td> 

                  <td className="py-3">

                    <span
                      className={`
                        px-3
                        py-1
                        rounded-full
                        text-white

                        ${
                          video.hook_score >= 80
                            ? "bg-green-500"
                            : video.hook_score >= 60
                            ? "bg-yellow-500"
                            : "bg-red-500"
                        }
                      `}
                    >
                      {video.hook_score}
                    </span>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}