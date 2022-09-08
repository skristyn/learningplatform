<template>
  <aside
    class="sidebar"
    :class="{ collapsed: collapseSidebar }"
    aria-label="Sidebar"
  >
    <!-- Sidebar header -->
    <div class="header">
      <!-- TODO replace these with the real API response values -->
      <div class="title">
        <h1 v-if="!collapseSidebar">
          {{ lessonNumber }}.{{ section?.number }} // {{ section?.title }}
        </h1>
      </div>
      <div class="exit">
        <!-- TODO: make this into a router-link -->
        <p @click="back" v-if="collapseSidebar">Exit</p>
        <p @click="back" v-else>Exit Lesson</p>
      </div>
    </div>

    <!-- Sidebar collapse icon -->
    <button class="collapse-icon" @click="toggleSidebar">
      <ion-icon name="chevron-back-outline"></ion-icon>
    </button>

    <!-- Notes -->
    <Notes v-if="showNotes" @close="toggleNotes" />

    <!-- Sidebar footer -->
    <!-- TODO find out what these buttons need to do -->
    <div class="button-container">
      <button aria-label="Chat" alt="Chat" title="Chat">
        <ion-icon
          class="button-icon"
          name="chatbubble-ellipses-outline"
        ></ion-icon>
        <p v-if="!collapseSidebar">chat</p>
      </button>
      <button
        aria-label="Notes"
        alt="Notes"
        title="Notes"
        :class="{ active: showNotes }"
        @click="toggleNotes"
      >
        <ion-icon name="reader-outline"></ion-icon>
        <p v-if="!collapseSidebar">notes</p>
      </button>
      <button aria-label="Message" alt="Message" title="Message">
        <ion-icon name="mail-open-outline"></ion-icon>
        <p v-if="!collapseSidebar">message</p>
      </button>
      <button aria-label="Tips" alt="Tips" title="Tips">
        <ion-icon name="bulb-outline"></ion-icon>
        <p v-if="!collapseSidebar">tips</p>
      </button>
    </div>
  </aside>
</template>

<script lang="ts">
import { computed, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import store from "@/store";
import Notes from "@/components/Notes.vue";

export default defineComponent({
  components: { Notes },
  setup() {
    const lessonNumber = computed(() => store.state.currentLesson?.number);
    const section = computed(() => store.state.currentSection);

    const router = useRouter();
    const back = () => {
      router.go(-1);
    };

    const collapseSidebar = ref(false);
    const showNotes = ref(false);

    const toggleSidebar = () => {
      // if the notes are open, close them
      // TODO should this warn about losing unsaved notes?
      if (showNotes.value) {
        toggleNotes();
      }
      // collapse the sidebar
      collapseSidebar.value = !collapseSidebar.value;
    };

    const toggleNotes = () => {
      // if the sidebar is collapsed, expand it
      if (collapseSidebar.value) {
        toggleSidebar();
      }
      // toggle whether or not to show the notes
      showNotes.value = !showNotes.value;
    };

    return {
      lessonNumber,
      section,
      collapseSidebar,
      showNotes,
      back,
      toggleSidebar,
      toggleNotes,
    };
  },
});
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-flow: column nowrap;
  justify-content: space-between;
  border-right: 3px solid var(--var-color-gray);
  color: var(--var-color-gray);
  margin: 0;
  width: 400px;
}

.header > * {
  border-bottom: 1px solid var(--var-color-gray);
  margin: 0;
}

.title {
  min-height: 172px;
}

.title h1 {
  font-size: 34px;
  padding: 75px 75px 30px;
  margin: 0;
}

.exit {
  padding: 0 75px;
}

.exit p {
  text-decoration: underline;
  color: royalblue;
  cursor: pointer;
}

.exit p:hover {
  text-decoration: none;
}

ion-icon {
  color: #9d9d9d;
  --ionicon-stroke-width: 28px;
}

.collapse-icon {
  align-self: flex-end;
  display: flex;
  background: none;
  border: 2px solid limegreen;
  border-right-width: 3px;
  border-radius: 16px 0 0 16px;
  padding: 16px 0;
  margin-right: -3px;
  cursor: pointer;
}

.collapse-icon ion-icon {
  font-size: 34px;
}

.button-container {
  display: flex;
  justify-content: center;
  border-top: 2px solid gray;
  padding: 0 20px 15px;
}

.button-container button {
  background: none;
  border: none;
  cursor: pointer;
  border-top-width: 6px;
  border-top-style: solid;
  padding: 26px 12px 1px;
  margin-top: -4px;
}

.button-container ion-icon {
  font-size: 58px;
  margin: 0 4px;
  cursor: pointer;
  pointer-events: none;
}

.button-container p {
  margin: 10px 0;
  color: gray;
  font-weight: 600;
}

.button-container button:nth-child(1) {
  border-top-color: salmon;
}

.button-container button:nth-child(1):hover,
.button-container button:nth-child(1):hover p,
.button-container button:nth-child(1):hover ion-icon {
  color: salmon;
}

.button-container button:nth-child(2) {
  border-top-color: limegreen;
}

.button-container button:nth-child(2):hover,
.button-container button:nth-child(2):hover p,
.button-container button:nth-child(2):hover ion-icon,
.button-container button:nth-child(2).active p,
.button-container button:nth-child(2).active ion-icon {
  color: limegreen;
}

.button-container button:nth-child(3) {
  border-top-color: royalblue;
}

.button-container button:nth-child(3):hover,
.button-container button:nth-child(3):hover p,
.button-container button:nth-child(3):hover ion-icon {
  color: royalblue;
}

.button-container button:nth-child(4) {
  border-top-color: darkturquoise;
}

.button-container button:nth-child(4):hover,
.button-container button:nth-child(4):hover p,
.button-container button:nth-child(4):hover ion-icon {
  color: darkturquoise;
}

/* when the sidebar is collapsed */

.sidebar.collapsed {
  width: 106px;
}

.sidebar.collapsed .exit {
  padding: 0;
  text-align: center;
}

.sidebar.collapsed .title h1 {
  visibility: hidden;
}

.sidebar.collapsed .collapse-icon {
  position: absolute;
  top: 330px;
  rotate: 180deg;
  left: 106px;
}

.sidebar.collapsed .button-container {
  flex-flow: column nowrap;
  border-top: none;
}

.sidebar.collapsed .button-container button {
  border-top: none;
  padding: 16px 0 0;
  margin: 0 0 16px;
}
</style>
