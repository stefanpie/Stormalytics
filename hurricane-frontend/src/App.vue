<template>
  <div id="app">
    <div class="main-grid">
      <Header />
      <SideBar />
    </div>
  </div>
</template>

<script>
import Header from "./components/Header";
import SideBar from "./components/SideBar";

export default {
  name: "App",
  components: {
    Header,
    SideBar
  }
};
</script>

<style>
html,
body {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  width: 100%;
  height: 100%;
}

.main-grid {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: 150px 1fr 1fr 1fr;
  grid-template-rows: 50px 1fr 1fr 1fr;
}

.header {
  width: 100%;
  height: 100%;
  grid-area: 1 / 1 / 2 / 5;
  background-color: lightskyblue;
  border-bottom: solid black 1px;
}

.side-bar {
  width: 100%;
  height: 100%;
  grid-area: 2 / 1 / 5 / 2;
  background-color: lightcyan;
  border-right: solid black 1px;
  border-top: solid black 1px;
  box-sizing: border-box;
}
</style>
