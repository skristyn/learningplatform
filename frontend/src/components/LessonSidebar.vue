<template>
  <aside
    class="sidebar"
    :class="{ collapsed: collapseSidebar }"
    aria-label="Sidebar"
  >
    <!-- Sidebar header -->
    <div class="sidebarHeader">
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

    <!-- Sidebar body -->
    <div class="sidebarBody">
      <!-- Notes or Tips -->
      <Notes v-if="showNotes" @close="toggleNotes" />
      <Tips v-else-if="showTips" @close="toggleTips" />
    </div>

    <!-- Sidebar footer -->
    <div class="sidebarFooter">
      <!-- TODO implement chat -->
      <!-- <button class="chat" aria-label="Chat" alt="Chat" title="Chat">
        <ion-icon
          class="button-icon"
          name="chatbubble-ellipses-outline"
        ></ion-icon>
        <p v-if="!collapseSidebar">chat</p>
      </button> -->

      <!-- TODO implement notes -->
      <!-- <button
        class="notes"
        aria-label="Click to open notes"
        alt="Notes page icon"
        title="Notes"
        :class="{ active: showNotes }"
        @click="toggleNotes"
      >
        <ion-icon name="reader-outline"></ion-icon>
        <p v-if="!collapseSidebar">notes</p>
      </button> -->

      <!-- TODO implement messaging -->
      <!-- <button class="message" aria-label="Message" alt="Message" title="Message">
        <ion-icon name="mail-open-outline"></ion-icon>
        <p v-if="!collapseSidebar">message</p>
      </button> -->

      <button
        class="tips"
        aria-label="Click to open tips"
        alt="Lightbult icon"
        title="Tips"
        :class="{ active: showTips }"
        @click="toggleTips"
      >
        <ion-icon name="bulb-outline"></ion-icon>
        <p v-if="!collapseSidebar">tips</p>
      </button>
    </div>
  </aside>

  <!-- Sidebar collapse icon -->
  <button
    class="collapseIcon"
    :class="{ collapsed: collapseSidebar }"
    @click="toggleSidebar"
  >
    <ion-icon name="chevron-back-outline"></ion-icon>
  </button>
</template>

<script lang="ts">
import { computed, defineComponent } from "vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import store from "@/store";
import Notes from "@/components/Notes.vue";
import Tips from "@/components/Tips.vue";

export default defineComponent({
  name: "LessonSidebar",
  components: { Notes, Tips },
  setup() {
    const lessonNumber = computed(() => store.state.currentLesson?.number);
    const section = computed(() => store.state.currentSection);

    const router = useRouter();
    const back = () => {
      router.go(-1);
    };

    const collapseSidebar = ref(false);
    const showNotes = ref(false);
    const showTips = ref(false);

    const toggleSidebar = () => {
      // if the notes or tips are open, close them
      // TODO should this warn about losing unsaved notes/tips?
      if (showNotes.value) {
        toggleNotes();
      }
      if (showTips.value) {
        toggleTips();
      }
      // collapse the sidebar
      collapseSidebar.value = !collapseSidebar.value;
    };

    const toggleNotes = () => {
      // if the sidebar is collapsed, expand it
      if (collapseSidebar.value) {
        toggleSidebar();
      }
      // if showing tips, hide them
      if (showTips.value) {
        toggleTips();
      }
      // toggle whether or not to show the notes
      showNotes.value = !showNotes.value;
    };

    const toggleTips = () => {
      // if the sidebar is collapsed, expand it
      if (collapseSidebar.value) {
        toggleSidebar();
      }
      // if showing notes, hide them
      if (showNotes.value) {
        toggleNotes();
      }
      // toggle whether or not to show the notes
      showTips.value = !showTips.value;
    };

    return {
      lessonNumber,
      section,
      collapseSidebar,
      showNotes,
      showTips,
      back,
      toggleSidebar,
      toggleNotes,
      toggleTips,
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
  flex: 1 0 auto;
}

.sidebarHeader > * {
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

.sidebarBody {
  padding: 0 38px 32px;
  margin-top: auto;
  overflow-y: auto;
}

.collapseIcon {
  cursor: pointer;
  background: none;
  border: 2px solid limegreen;
  border-right-width: 3px;
  border-radius: 16px 0 0 16px;
  padding: 16px 0;
  margin-top: auto;
  margin-bottom: 240px;
  margin-left: -39px;
}

.collapseIcon ion-icon {
  font-size: 34px;
}

.sidebarFooter {
  display: flex;
  justify-content: center;
  border-top: 2px solid gray;
  padding: 0 20px 15px;
}

.sidebarFooter button {
  background: none;
  border: none;
  cursor: pointer;
  border-top-width: 6px;
  border-top-style: solid;
  padding: 26px 12px 1px;
  margin-top: -4px;
}

.sidebarFooter ion-icon {
  font-size: 58px;
  margin: 0 4px;
  cursor: pointer;
  pointer-events: none;
}

.sidebarFooter p {
  margin: 10px 0;
  color: gray;
  font-weight: 600;
}

.sidebarFooter .chat {
  border-top-color: salmon;
}

.sidebarFooter .chat:hover,
.sidebarFooter .chat:hover p,
.sidebarFooter .chat:hover ion-icon {
  color: salmon;
}

.sidebarFooter .notes {
  border-top-color: limegreen;
}

.sidebarFooter .notes:hover,
.sidebarFooter .notes:hover p,
.sidebarFooter .notes:hover ion-icon,
.sidebarFooter .notes.active p,
.sidebarFooter .notes.active ion-icon {
  color: limegreen;
}

.sidebarFooter .message {
  border-top-color: royalblue;
}

.sidebarFooter .message:hover,
.sidebarFooter .message:hover p,
.sidebarFooter .message:hover ion-icon {
  color: royalblue;
}

.sidebarFooter .tips {
  border-top-color: darkturquoise;
}

.sidebarFooter .tips:hover,
.sidebarFooter .tips:hover p,
.sidebarFooter .tips:hover ion-icon,
.sidebarFooter .tips.active p,
.sidebarFooter .tips.active ion-icon {
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

.collapseIcon.collapsed {
  rotate: 180deg;
  margin-left: -3px;
}

.sidebar.collapsed .sidebarFooter {
  flex-flow: column nowrap;
  border-top: none;
}

.sidebar.collapsed .sidebarFooter button {
  border-top: none;
  padding: 16px 0 0;
  margin: 0 0 16px;
}
</style>
