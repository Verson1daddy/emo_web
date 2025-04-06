document.getElementById("submitBtn").addEventListener("click", () => {
  const textArea = document.querySelector(".bubble-text");
  const content = textArea.value.trim();

  if (!content) {
    alert("内容不能为空");
    return;
  }

  fetch("/analysis/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ emotion_input: content }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.errors) {
        alert("提交失败：" + JSON.stringify(data.errors));
      } else {
        window.location.href = `/output/?emotion_analysis=${encodeURIComponent(
          data.emotion_analysis
        )}&comfort=${encodeURIComponent(data.comfort)}`;
      }
    })
    .catch((error) => {
      console.error("请求失败：", error);
      alert("请求失败，请稍后再试。");
    });
});
