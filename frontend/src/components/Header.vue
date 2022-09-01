<template>
  <header :class="{ headerBackground: needsHeaderBackground }">
    <router-link :to="{ name: isLoggedIn ? 'Home' : 'Login' }" class="title">
      <h2 alt="Learning Platform">learning<br />platform</h2>
    </router-link>
    <div class="buttons" v-if="isLoggedIn">
      <button aria-label="Community" alt="Community" title="Community">
        <ion-icon name="people-outline"></ion-icon>
      </button>

      <!-- Use Floating Vue library to create the dropdown menu with log out & other options -->
      <VDropdown :distance="6">
        <!-- This is the popover reference (for the events and position) -->
        <button aria-label="Profile" alt="Profile" title="Profile">
          <ion-icon name="person-circle-outline"></ion-icon>
        </button>

        <!-- This will be the content of the popover -->
        <template #popper>
          <div class="dropdownMenu">
            <p @click="logOut">Log out</p>
          </div>
        </template>
      </VDropdown>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Header",
  computed: {
    isLoggedIn() {
      return this.$store.state.isAuthenticated;
    },
    needsHeaderBackground() {
      const needsHeaderBackground = !(
        this.$route.name == "Login" || this.$route.name == "Home"
      );
      return needsHeaderBackground;
    },
  },
  methods: {
    async logOut() {
      if (this.$store.state.isAuthenticated) {
        await this.$store.commit("logOut");

        if (!this.$store.state.isAuthenticated) {
          this.$router.push({ name: "Login" });
        }
      }
    },
  },
});
</script>

<style scoped>
header {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
  padding: 30px;
}

.headerBackground {
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' height='100%25' width='100%25'%3E%3Cdefs%3E%3Cpattern id='doodad' width='75' height='75' viewBox='0 0 40 40' patternUnits='userSpaceOnUse' patternTransform='rotate(90)'%3E%3Crect width='100%25' height='100%25' fill='rgba(255, 255, 255, 1)'/%3E%3Cpath d='M-0.5 20v20h1v-20zM19.5 20v20h1v-20zM39.5 20v20h1v-20z' fill='rgba(226, 232, 240, 1)' filter='url(%23filter-doodad-1)'/%3E%3Cpath d='M-10 29.5 h60 v1 h-60z' fill='rgba(226, 232, 240, 1)'/%3E%3Cpath d='M9.5 0v40h1v-40zM29.5 0v40h1v-40z' fill='rgba(226, 232, 240, 1)' filter='url(%23filter-doodad-1)'/%3E%3Cpath d='M-10 9.5h60v1h-60z' fill='rgba(226, 232, 240, 1)'/%3E%3Cpath d='M-0.5 0v20h1v-20zM19.5 0v20h1v-20zM39.5 0v20h1v-20z' fill='rgba(226, 232, 240, 1)' filter='url(%23filter-doodad-1)'/%3E%3C/pattern%3E%3Cfilter id='filter-doodad-1'%3E%3CfeTurbulence baseFrequency='0.01 0' numOctaves='2' result='result1'/%3E%3CfeDisplacementMap in2='result1' scale='0' result='result2' xChannelSelector='R' yChannelSelector='G' in='SourceGraphic'/%3E%3CfeComposite in2='result2' in='SourceGraphic' operator='atop' result='compositeGraphic'/%3E%3CfeOffset in='compositeGraphic' result='fbSourceGraphic' dx='0'/%3E%3C/filter%3E%3C/defs%3E%3Crect fill='url(%23doodad)' height='200%25' width='200%25'/%3E%3C/svg%3E ");
}

.title {
  text-decoration: none;
  color: inherit;
}

.title h2 {
  margin: 0;
}

.buttons {
  display: flex;
  align-items: center;
}

.buttons button {
  background: none;
  border: none;
  cursor: pointer;
}

.buttons ion-icon {
  height: 46px;
  width: 46px;
  margin: 0 4px;
  cursor: pointer;
  pointer-events: none;
}

/* Profile dropdown menu */
.dropdownMenu {
  padding: 10px;
}

.dropdownMenu p {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-style: italic;
  color: var(--var-color-almost-black);
  margin: 0;
  padding: 6px;
  transition: 0.15s;
}

.dropdownMenu p:hover {
  cursor: pointer;
  background-color: var(--var-color-gray-lighter);
}
</style>
