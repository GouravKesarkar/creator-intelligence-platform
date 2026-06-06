import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getVideoDetails } from "../api/creatorApi";

export default function VideoDetails() {

  const { videoId } = useParams();
  const navigate = useNavigate();

  const [data, setData] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {

    try {

      const response =
        await getVideoDetails(videoId);

      setData(response.data);

    } catch (error) {

      console.error(error);
    }
  }

  if (!data) {

    return (
      <div className="p-8 text-xl">
        Loading...
      </div>
    );
  }

  const video = data.video;
  const commentAnalysis = data.comment_analysis;
  const hookAnalysis = data.hook_analysis;

  return (

    <div className="
      min-h-screen
      bg-slate-100
      p-8
    ">

      <div className="
        max-w-6xl
        mx-auto
      ">

        {/* Header */}

        <div className="
          flex
          justify-between
          items-center
          mb-8
        ">

          <h1 className="
            text-4xl
            font-bold
          ">
            Video Intelligence
          </h1>

          <button
            onClick={() => navigate("/")}
            className="
              bg-blue-600
              text-white
              px-4
              py-2
              rounded-lg
              hover:bg-blue-700
            "
          >
            Back
          </button>

        </div>

        {/* Video Overview */}

        <div className="
          bg-white
          rounded-xl
          shadow-md
          p-6
          mb-8
        ">

          <div className="
            flex
            flex-col
            md:flex-row
            gap-6
          ">

            <img
              src={video.thumbnail_url}
              alt={video.title}
              className="
                w-full
                md:w-96
                rounded-lg
              "
            />

            <div className="flex-1">

              <h2 className="
                text-3xl
                font-bold
                mb-2
              ">
                {video.title}
              </h2>

              <p className="
                text-gray-600
                mb-4
              ">
                {video.channel_name}
              </p>

              <div className="
                grid
                grid-cols-2
                md:grid-cols-4
                gap-4
              ">

                <div className="
                  bg-slate-50
                  p-4
                  rounded-lg
                ">
                  <div className="text-sm text-gray-500">
                    Views
                  </div>
                  <div className="text-xl font-bold">
                    {video.views}
                  </div>
                </div>

                <div className="
                  bg-slate-50
                  p-4
                  rounded-lg
                ">
                  <div className="text-sm text-gray-500">
                    Likes
                  </div>
                  <div className="text-xl font-bold">
                    {video.likes}
                  </div>
                </div>

                <div className="
                  bg-slate-50
                  p-4
                  rounded-lg
                ">
                  <div className="text-sm text-gray-500">
                    Comments
                  </div>
                  <div className="text-xl font-bold">
                    {video.comments}
                  </div>
                </div>

                <div className="
                  bg-slate-50
                  p-4
                  rounded-lg
                ">
                  <div className="text-sm text-gray-500">
                    Published
                  </div>
                  <div className="text-sm font-bold">
                    {video.published_at}
                  </div>
                </div>

              </div>

            </div>

          </div>

        </div>

        {/* Audience Intelligence */}

        {commentAnalysis && (

          <div className="
            bg-white
            rounded-xl
            shadow-md
            p-6
            mb-8
          ">

            <h2 className="
              text-2xl
              font-bold
              mb-6
            ">
              Audience Intelligence
            </h2>

            <div className="mb-6">

              <span className="
                px-4
                py-2
                rounded-full
                bg-blue-600
                text-white
                font-semibold
              ">
                {commentAnalysis.overall_sentiment}
              </span>

            </div>

            {/* Top Topics */}

            <div className="mb-6">

              <h3 className="
                text-lg
                font-bold
                mb-3
              ">
                Top Topics
              </h3>

              <div className="
                flex
                flex-wrap
                gap-2
              ">

                {commentAnalysis.top_topics?.map(
                  (topic, index) => (
                    <span
                      key={index}
                      className="
                        bg-slate-200
                        px-3
                        py-1
                        rounded-full
                      "
                    >
                      {topic}
                    </span>
                  )
                )}

              </div>

            </div>

            {/* Viewer Questions */}

            <div className="mb-6">

              <h3 className="
                text-lg
                font-bold
                mb-3
              ">
                Viewer Questions
              </h3>

              <ul className="
                list-disc
                pl-5
              ">

                {commentAnalysis.viewer_questions?.map(
                  (question, index) => (
                    <li key={index}>
                      {question}
                    </li>
                  )
                )}

              </ul>

            </div>

            {/* Summary */}

            <div>

              <h3 className="
                text-lg
                font-bold
                mb-3
              ">
                AI Summary
              </h3>

              <div className="
                bg-slate-50
                p-4
                rounded-lg
              ">
                {commentAnalysis.summary}
              </div>

            </div>

          </div>

        )}

        {/* Hook Analysis */}

        {hookAnalysis && (

          <div className="
            bg-white
            rounded-xl
            shadow-md
            p-6
            mb-8
          ">

            <h2 className="
              text-2xl
              font-bold
              mb-6
            ">
              Hook Intelligence
            </h2>

            <div className="
              grid
              grid-cols-2
              md:grid-cols-5
              gap-4
              mb-8
            ">

              <div className="bg-slate-50 p-4 rounded-lg">
                <div className="text-sm">Hook</div>
                <div className="text-2xl font-bold">
                  {hookAnalysis.hook_score}
                </div>
              </div>

              <div className="bg-slate-50 p-4 rounded-lg">
                <div className="text-sm">Curiosity</div>
                <div className="text-2xl font-bold">
                  {hookAnalysis.curiosity_score}
                </div>
              </div>

              <div className="bg-slate-50 p-4 rounded-lg">
                <div className="text-sm">Engagement</div>
                <div className="text-2xl font-bold">
                  {hookAnalysis.engagement_score}
                </div>
              </div>

              <div className="bg-slate-50 p-4 rounded-lg">
                <div className="text-sm">Clarity</div>
                <div className="text-2xl font-bold">
                  {hookAnalysis.clarity_score}
                </div>
              </div>

              <div className="bg-slate-50 p-4 rounded-lg">
                <div className="text-sm">Retention</div>
                <div className="text-2xl font-bold">
                  {hookAnalysis.retention_score}
                </div>
              </div>

            </div>

            <div className="
              grid
              md:grid-cols-3
              gap-6
            ">

              <div>

                <h3 className="
                  font-bold
                  mb-3
                ">
                  Strengths
                </h3>

                <ul className="list-disc pl-5">

                  {hookAnalysis.strengths?.map(
                    (item, index) => (
                      <li key={index}>
                        {item}
                      </li>
                    )
                  )}

                </ul>

              </div>

              <div>

                <h3 className="
                  font-bold
                  mb-3
                ">
                  Weaknesses
                </h3>

                <ul className="list-disc pl-5">

                  {hookAnalysis.weaknesses?.map(
                    (item, index) => (
                      <li key={index}>
                        {item}
                      </li>
                    )
                  )}

                </ul>

              </div>

              <div>

                <h3 className="
                  font-bold
                  mb-3
                ">
                  Recommendations
                </h3>

                <ul className="list-disc pl-5">

                  {hookAnalysis.recommendations?.map(
                    (item, index) => (
                      <li key={index}>
                        {item}
                      </li>
                    )
                  )}

                </ul>

              </div>

            </div>

          </div>

        )}

      </div>

    </div>

  );
}