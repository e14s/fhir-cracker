import logo from './logo.svg';
import './App.css';
import './component/UploadImageToS3WithNativeSdk'
import UploadImageToS3WithNativeSdk from "./component/UploadImageToS3WithNativeSdk";
import UploadImageToS3WithReactS3 from "./component/UploadImageToS3WithReactS3";

function App() {
  return (
    <div className="App">
      <UploadImageToS3WithNativeSdk></UploadImageToS3WithNativeSdk>
    </div>
  );
}

export default App;
