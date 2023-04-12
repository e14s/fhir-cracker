import React ,{useState} from 'react';
import AWS from 'aws-sdk'
import {
    SecretsManagerClient,
    GetSecretValueCommand,
} from "@aws-sdk/client-secrets-manager";

const S3_BUCKET ='fhir-cracker-file-upload';
const REGION ='us-east-1';


const UploadImageToS3WithNativeSdk = () => {

    const [progress , setProgress] = useState(0);
    const [selectedFile, setSelectedFile] = useState(null);
    const [accessKey, setAccessKey] = useState(null);
    const [secretKey, setSecretKey] = useState(null);

    const handleFileInput = (e) => {
        setSelectedFile(e.target.files[0]);
    }

    const handleSecretKey = (e) => {
        setSecretKey(e.target.value);
    }

    const handleAccessKey = (e) => {
        setAccessKey(e.target.value);
    }
    const uploadFile = (file) => {

        AWS.config.update({
            accessKeyId: accessKey,
            secretAccessKey: secretKey
        })

        const myBucket = new AWS.S3({
            params: { Bucket: S3_BUCKET},
            region: REGION,
        })
        const params = {
            ACL: 'public-read',
            Body: file,
            Bucket: S3_BUCKET,
            Key: file.name
        };

        myBucket.putObject(params)
            .on('httpUploadProgress', (evt) => {
                setProgress(Math.round((evt.loaded / evt.total) * 100))
            })
            .send((err) => {
                if (err) console.log(err)
            })
    }


    return <div>
        <div>Secured Native SDK File Upload Progress is {progress}%</div>
        <div>
            <input type="text" id="accessKey" title="Enter AWS Access Key" onChange={handleAccessKey}/>
            <input type="text" id="secretKey" title="Enter AWS Secret Key" onChange={handleSecretKey}/>
        </div>
        <div><input type="file" onChange={handleFileInput}/></div>
        <div><button onClick={() => uploadFile(selectedFile)}> Upload to S3</button></div>
    </div>
}

export default UploadImageToS3WithNativeSdk;