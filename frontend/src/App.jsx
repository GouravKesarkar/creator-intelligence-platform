import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import VideoDetails from "./pages/VideoDetails";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Dashboard />}
        />

        <Route
          path="/video/:videoId"
          element={<VideoDetails />}
        />

      </Routes>

    </BrowserRouter>

  );
}

export default App;