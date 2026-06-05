export default function Sidebar() {

  return (

    <div className="
      w-64
      bg-slate-900
      text-white
      min-h-screen
      p-6
    ">

      <h1 className="
        text-xl
        font-bold
        mb-10
      ">
        Creator IQ
      </h1>

      <ul className="space-y-4">

        <li className="hover:text-blue-400 cursor-pointer">
          Dashboard
        </li>

        <li className="hover:text-blue-400 cursor-pointer">
          Videos
        </li>

        <li className="hover:text-blue-400 cursor-pointer">
          Trends
        </li>

        <li className="hover:text-blue-400 cursor-pointer">
          Analyze
        </li>

      </ul>

    </div>

  )
}