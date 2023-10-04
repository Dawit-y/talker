const btn = document
  .getElementById("some")
  .addEventListener("click", async function getData(event) {
    await fetch(`request/${event.target.value}/`)
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        console.log(data);
      });
  });
