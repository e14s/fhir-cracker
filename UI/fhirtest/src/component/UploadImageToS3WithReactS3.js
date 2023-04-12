import React , {useState} from 'react';
import { uploadFile } from 'react-s3';
import { Buffer } from "buffer";


Buffer.from("anything", "base64");
window.Buffer = window.Buffer || require("buffer").Buffer;

const S3_BUCKET ='fhir-cracker-file-upload';
const REGION ='us-east-1';
const ACCESS_KEY = 'ACCESS_KEY';
const SECRET_ACCESS_KEY ='SECRET_ACCESS_KEY';

const config = {
    bucketName: S3_BUCKET,
    region: REGION,
    accessKeyId: ACCESS_KEY,
    secretAccessKey: SECRET_ACCESS_KEY,
}

const UploadImageToS3WithReactS3 = () => {

    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileInput = (e) => {
        setSelectedFile(e.target.files[0]);
    }

    const handleUpload = async (file) => {
        uploadFile(file, config)
            .then(data => console.log(data))
            .catch(err => console.error(err))
    }

    return <div>
        <div>React S3 File Upload</div>
        <input type="file" onChange={handleFileInput}/>
        <button onClick={() => handleUpload(selectedFile)}> Upload to S3</button>
    </div>
}

export default UploadImageToS3WithReactS3;