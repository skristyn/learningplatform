<template>
<div class="landing-grid">
    <div class="welcomeLeft">
      <DPageTitle title="Welcome!" />
      <p>Just adding some test text to see how this will look on the page. A random encouraging phrase will go here.</p>
    </div>
    <div class="welcomeRight">
      <h3>Want to continue where you left off?</h3>
      <div style="display: inline-block;"><button id="continue-button">1:5 Name of Lesson</button></div>
      <div class="overview-link"><p>Or, <router-link to="/course-dashboard">go to course overview</router-link></p></div>
    </div>
  <div class="announcement" v-if="user">
    Announcement: {{ user.announcement }}
  </div>

  <div class="resource">
    <div class="resource-relative">
      <img src="../assets/home-left-pattern.svg" />
      <div id="resource-link"><a href="#">Resource Kit</a></div>
    </div>
  </div>
  <div class="community">
    <div class="community-relative">
      <img src="../assets/home-right-pattern.svg" />
      <div id="community-link"><a href="#">Community</a></div>
    </div>
  </div>
  <!-- TODO: create these buttons when the following links exist -->
  <!-- <div class="links">
    <div class="resource">
      <router-link to="/resource-kit">Resource Kit</router-link>
    </div>
    <div class="community">
      <router-link to="/community">Community</router-link>
    </div>
  </div> -->
</div> <!-- end landing-grid -->
</template>

<script lang="ts">
import { defineComponent } from "vue";
import DPageTitle from "@/components/DPageTitle.vue";

export default defineComponent({
  name: "Home",
  components: {
    DPageTitle,
  },
  async mounted() {
    this.$store.dispatch("getUserData");
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
  },
});
</script>

<style lang="scss" scoped>
.landing-grid {
  display: grid;
  grid-template-columns: minmax(30px, 1fr) minmax(30px, 1fr) minmax(30px, 1fr) minmax(30px, 1fr) minmax(30px, 1fr) minmax(30px, 1fr) minmax(30px, 1fr) minmax(30px, 1fr) minmax(30px, 1fr) minmax(30px, 1fr) minmax(30px, 1fr) minmax(30px, 1fr);
  grid-template-rows: auto;
  grid-template-areas:
    "welcome welcome welcome welcome welcome continue continue continue continue continue continue continue"
    "announcement announcement announcement announcement announcement announcement announcement announcement announcement announcement announcement announcement"
    "resource resource resource resource resource resource community community community community community community";
  column-gap: 1rem;
  row-gap: 2rem;
}

@media screen and (max-width: 850px) {
  .landing-grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      "welcome"
      "continue"
      "announcement"
      "resource"
      "community";
  }
}

.welcomeLeft {
  margin-bottom: 76px;
  grid-area: welcome;
  padding-right: 50px;
}

.welcomeLeft p {
  font-size: 1.2rem;
  font-weight: 500;
}

.resource {
  grid-area: resource;
}

.resource img {
}

#resource-link {
  position: absolute;
  bottom: 0;
  right: 4vw;
}

.community {
  grid-area: community;
  text-align: right;
}

.community img {
  width: 55%;
  margin-top: 10vw;
}

.resource-relative {
  position: relative;
  width: 60%;
}

.community-relative {
  position: relative;
}

.welcomeRight {
  grid-area: continue;
  background-image: url('../assets/home-continue-pattern.svg');
  background-position: top left;
  background-size: 100% auto;
  background-repeat: no-repeat;
  min-height: 25.5vw;
  padding-left: 20vw;
  h3 {
    font-weight: 900;
    margin-top: 32px;
    margin-bottom: 38px;
  }
}

.welcomeRight p {
  font-weight: bold;
  font-size: 1.3rem;
  margin-top: 0;
}

.welcomeRight a:visited {
  color: var(--var-color-blue-dark);
}

.announcement {
  grid-area: announcement;
  background-color: var(--var-color-gray-lighter);
  margin-left: -5vw;
  margin-right: -5vw;
  padding: 26px 40px;
  text-align: center;
  font-size: 1.6rem;
  font-weight: 500;
  margin-bottom: 9vw;
}

#continue-button {
  height: 2.9em;
  border: 7px solid;
  border-image: url('../assets/pink-stamp-button.svg') 33;
  border-image-width: 28px;
  background: #fff;
  cursor: pointer;
  line-height: .15rem;
  font-weight: 700;
  color: #F15882;
  font-size: 1.3rem;
  margin-right: 25px;
  border-image-outset: 1;
  float: left;
  padding: 0 10px;
}

.overview-link {
  display: inline-block;
  width: 40%;
}
</style>