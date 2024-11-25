// const apiBase = ""; // 使用相对路径
// const apiBase = "http://localhost:4568"; // 替换为你的后端地址

// 保存当前选中的封面图ID
let selectedThumbMediaId = '';

// 页面加载完成后立即获取列表
document.addEventListener('DOMContentLoaded', () => {
    getMaterialList();
    getDraftList();
});

// TinyMCE初始化
tinymce.init({
    selector: '#draft-data',
    plugins: [
        'anchor', 'autolink', 'charmap', 'codesample', 'emoticons', 'image',
        'link', 'lists', 'media', 'searchreplace', 'table', 'visualblocks',
        'wordcount',
        'checklist', 'mediaembed', 'casechange', 'formatpainter'
    ],

    toolbar: [
        'undo redo | blocks fontfamily fontsize',
        'bold italic underline strikethrough | link image media table',
        'alignleft aligncenter alignright | lineheight',
        'checklist numlist bullist | indent outdent',
        'removeformat'
    ].join(' | '),

    height: 500,
    menubar: false,
    statusbar: false,
    placeholder: '从这里开始写正文',

    // 图片上传相关配置
    images_upload_handler: function (blobInfo, progress) {
        return new Promise((resolve, reject) => {
            const formData = new FormData();
            formData.append('file', blobInfo.blob());

            fetch('/api/v1/materials/add_material', {
                method: 'POST',
                body: formData
            })
                .then(async response => {
                    const result = await response.json();
                    if (!response.ok) {
                        throw new Error(result.message || '上传失败');
                    }

                    if (result.data && result.data.url) {
                        // 上传成功后刷新素材列表
                        getMaterialList();
                        // 返回图片URL
                        resolve(result.data.url);
                    } else {
                        throw new Error('上传成功但未获得图片URL');
                    }
                })
                .catch(error => {
                    console.error("上传素材失败:", error);
                    reject(error.message || '上传失败');
                });
        });
    },

    // 自动上传粘贴的图片
    paste_data_images: true,

    // 图片文件选择配置
    file_picker_types: 'image',
    file_picker_callback: function (callback, value, meta) {
        if (meta.filetype === 'image') {
            const input = document.createElement('input');
            input.setAttribute('type', 'file');
            input.setAttribute('accept', 'image/*');

            input.onchange = function () {
                const file = this.files[0];
                const formData = new FormData();
                formData.append('file', file);

                fetch('/api/v1/materials/add_material', {
                    method: 'POST',
                    body: formData
                })
                    .then(async response => {
                        const result = await response.json();
                        if (!response.ok) {
                            throw new Error(result.message || '上传失败');
                        }

                        if (result.data && result.data.url) {
                            // 上传成功后刷新素材列表
                            getMaterialList();
                            // 插入图片
                            callback(result.data.url, { title: file.name });
                        } else {
                            throw new Error('上传成功但未获得图片URL');
                        }
                    })
                    .catch(error => {
                        console.error("上传素材失败:", error);
                        alert('上传失败: ' + (error.message || '未知错误'));
                    });
            };

            input.click();
        }
    },

    // 基础样式配置
    content_style: `
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, 
                        Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
            font-size: 16px;
            line-height: 1.6;
            padding: 15px;
        }
        img { max-width: 100%; height: auto; }
        p { margin: 0 0 1em 0; }
        table { width: 100%; border-collapse: collapse; }
        table td, table th { border: 1px solid #ccc; padding: 0.4em; }
    `,

    // 其他设置
    browser_spellcheck: true,
    contextmenu: false,
    elementpath: false,
    resize: false,
});
// 保存草稿
document.getElementById('save-draft-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    if (!selectedThumbMediaId) {
        alert('请选择封面图片');
        return;
    }

    const title = document.getElementById('article-title').value;
    const author = document.getElementById('article-author').value;
    const content = tinymce.get('draft-data').getContent();
    const digest = content.replace(/<[^>]+>/g, '').slice(0, 100); // 获取纯文本的前100个字符作为摘要

    // 构建要保存的数据
    const draftData = {
        articles: [{
            title,
            author,
            digest,
            content,
            content_source_url: '',
            thumb_media_id: selectedThumbMediaId,
            need_open_comment: 0,
            only_fans_can_comment: 0
        }]
    };

    try {
        const response = await fetch(`/api/v1/wechat/save_draft`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(draftData)
        });

        const result = await response.json();
        document.getElementById('save-draft-response').textContent = JSON.stringify(result, null, 2);

        // 保存成功后刷新草稿列表
        getDraftList();
    } catch (error) {
        console.error('保存草稿失败:', error);
    }
});
// 上传素材
document.getElementById("upload-material-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById("material-file");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch(`/api/v1/materials/add_material`, {
            method: "POST",
            body: formData
        });
        const result = await response.json();
        document.getElementById("upload-material-response").textContent = JSON.stringify(result, null, 2);
        // 上传成功后刷新素材列表
        getMaterialList();
    } catch (error) {
        console.error("上传素材失败:", error);
    }
});

// 获取素材列表
async function getMaterialList() {
    try {
        const response = await fetch(`/api/v1/materials/get_material_list`);
        const result = await response.json();

        const materialList = document.getElementById("material-list");
        materialList.innerHTML = '<div class="material-list">'; // 使用网格布局包装器

        result.data.item.forEach(material => {
            const div = document.createElement("div");
            div.className = "material-item" + (material.media_id === selectedThumbMediaId ? ' selected' : '');
            div.innerHTML = `
                <img src="${material.url}" alt="${material.name}" />
                <p>${material.name}</p>
            `;

            // 单击选择封面图
            div.addEventListener("click", (e) => {
                // 移除所有其他项目的选中状态
                document.querySelectorAll('.material-item').forEach(item => {
                    item.classList.remove('selected');
                });
                // 添加当前项目的选中状态
                div.classList.add('selected');
                selectedThumbMediaId = material.media_id;
                e.preventDefault(); // 阻止冒泡，避免触发双击
            });

            // 双击插入图片到编辑器
            div.addEventListener("dblclick", () => {
                tinymce.activeEditor.insertContent(`<img src="${material.url}" alt="${material.name}" />`);
            });

            materialList.querySelector('.material-list').appendChild(div);
        });
    } catch (error) {
        console.error("获取素材列表失败:", error);
    }
}

// 获取草稿列表
async function getDraftList() {
    try {
        const response = await fetch(`/api/v1/wechat/get_draft_list?offset=0&count=20`);
        const result = await response.json();

        const draftList = document.getElementById("draft-list");
        draftList.innerHTML = ''; // 清空当前内容

        if (result.data && result.data.item) {
            result.data.item.forEach(draft => {
                const firstNewsItem = draft.content.news_item[0];
                const updateTime = new Date(draft.update_time * 1000).toLocaleString();

                const div = document.createElement("div");
                div.className = "draft-item";
                div.innerHTML = `
                    <h4>${firstNewsItem.title}</h4>
                    <p>更新时间: ${updateTime}</p>
                    <div class="draft-actions">
                        <button class="edit" onclick="editDraft('${draft.media_id}')">编辑</button>
                        <button class="delete" onclick="deleteDraft('${draft.media_id}')">删除</button>
                    </div>
                `;

                // 为整个草稿项添加点击事件（不包括按钮）
                div.addEventListener("click", (e) => {
                    // 如果点击的不是按钮，则选择该草稿
                    if (!e.target.matches('button')) {
                        selectDraft(draft.media_id);
                    }
                });

                draftList.appendChild(div);
            });
        }
    } catch (error) {
        console.error("获取草稿列表失败:", error);
    }
}

// 刷新按钮事件监听
document.getElementById("refresh-material-list").addEventListener("click", getMaterialList);
document.getElementById("refresh-draft-list").addEventListener("click", getDraftList);

// 选择草稿
function selectDraft(mediaId) {
    document.getElementById("media-id").value = mediaId;
    document.getElementById("schedule-media-id").value = mediaId;
    console.log("Selected draft:", mediaId);
}

// 编辑草稿
function editDraft(mediaId) {
    console.log("Editing draft:", mediaId);
    // 实现编辑功能
}

// 删除草稿
function deleteDraft(mediaId) {
    if (confirm("确定要删除这个草稿吗？")) {
        console.log("Deleting draft:", mediaId);
        // 实现删除功能
    }
}

// 群发推送
document.getElementById('send-mass-message-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const mediaId = document.getElementById('media-id').value;
    const tagId = document.getElementById('tag-id').value;

    // 构建查询参数
    const params = new URLSearchParams({
        is_to_all: 'true',  // 统一设置为true
        media_id: mediaId
    });

    // 如果有tag_id，添加到查询参数中
    if (tagId) {
        params.append('tag_id', tagId);
    }

    try {
        const response = await fetch(`/api/v1/wechat/send_mass_message?${params.toString()}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const result = await response.json();
        document.getElementById('send-mass-message-response').textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        console.error('群发消息失败:', error);
        document.getElementById('send-mass-message-response').textContent = '群发消息失败: ' + error.message;
    }
});

// 定时群发推送
document.getElementById('schedule-mass-message-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const scheduleTime = document.getElementById('schedule-time').value;
    const mediaId = document.getElementById('schedule-media-id').value;
    const tagId = document.getElementById('schedule-tag-id').value;

    // 构建查询参数
    const params = new URLSearchParams({
        is_to_all: 'true',  // 统一设置为true
        media_id: mediaId,
        datetime: new Date(scheduleTime).toISOString()
    });

    // 如果有tag_id，添加到查询参数中
    if (tagId) {
        params.append('tag_id', tagId);
    }

    try {
        const response = await fetch(`/api/v1/wechat/timed_send_mass_message?${params.toString()}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const result = await response.json();
        document.getElementById('schedule-mass-message-response').textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        console.error('定时群发消息失败:', error);
        document.getElementById('schedule-mass-message-response').textContent = '定时群发消息失败: ' + error.message;
    }
});