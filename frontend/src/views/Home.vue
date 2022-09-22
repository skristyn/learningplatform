<template>
  <div class="welcome">
    <div class="welcomeLeft">
      <DPageTitle title="Welcome!" />
    </div>
    <div class="welcomeRight">
      <h3>Want to continue where you left off?</h3>
      <router-link to="/course-dashboard">Go to course overview</router-link>
    </div>
  </div>
  <div class="announcement" v-if="user">
    Announcement: {{ user.announcement }}
  </div>
  <!-- TODO: create these buttons when the following links exist -->
  <!-- <div class="links">
    <router-link to="/resource-kit">Resource Kit</router-link>
    <router-link to="/community">Community</router-link>
  </div> -->
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

<style scoped>
.welcome {
  display: flex;
  flex-flow: row wrap;
  margin-bottom: 76px;
}

.welcomeLeft,
.welcomeRight {
  flex: 1 0 auto;
}

.welcomeRight h3 {
  font-weight: 900;
}

.welcomeRight a {
  font-weight: bold;
  font-size: 24px;
}

.welcomeRight a:visited {
  color: var(--var-color-blue-dark);
}

.announcement {
  background-color: var(--var-color-gray-lighter);
  margin-left: -40px;
  margin-right: -40px;
  padding: 26px 40px;
  text-align: center;
  font-size: 26px;
  font-weight: 500;
}
</style>
