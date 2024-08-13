document.getElementById('upload-btn').addEventListener('click', uploadFiles);

async function uploadFiles() {
    const files = document.getElementById('file-upload').files;
    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    try {
        const response = await fetch('/api/v1/uploadfile/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const result = await response.json();
        console.log('Upload successful:', result);
        alert("Upload Completed"); // 弹出提示框
    } catch (error) {
        console.error('Error during file upload:', error);
        alert("Upload failed"); // 上传失败时的提示
    }
}
