<template>
  <p v-if="!textbook">Loading...</p>

  <div v-else>
    <PageHeader :title="textbook.title" />

    <!-- TODO add progress bar -->
    <!-- TODO add button to continue latest lesson -->

    <!-- when Tabs emits the onSelectedTab event, take its tabTitle and set selectedTab state to this string value -->
    <Tabs
      :tabs="tabs"
      :selectedTab="selectedTab"
      @onSelectTab="selectedTab = $event"
    />

    <!-- One of the following three will display based on tab selection -->
    <LessonList v-if="selectedTab === 'Lessons'" :lessons="textbook.lessons" />
    <div v-if="selectedTab === 'Resources'">
      <p>resources placeholder</p>
    </div>
    <div v-if="selectedTab === 'Project'">
      <p>project placeholder</p>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, reactive, toRefs } from "vue";
import PageHeader from "@/components/PageHeader.vue"; // @ is an alias to /src
import Tabs from "@/components/Tabs.vue";
import store from "@/store";
import LessonList from "@/components/LessonList.vue";

export default defineComponent({
  name: "CourseDashboard",
  components: {
    PageHeader,
    Tabs,
    LessonList,
  },
  setup() {
    const tabs = [
      { ionIconName: "book-outline", tabTitle: "Lessons" },
      { ionIconName: "briefcase-outline", tabTitle: "Resources" },
      { ionIconName: "clipboard-outline", tabTitle: "Project" },
    ];

    // the default tab is always Lessons
    const state = reactive({
      selectedTab: "Lessons",
    });

    store.dispatch("getDigitalStewardTextbook");
    const textbook = computed(() => store.state.textbook);

    // We want to expand the first incomplete lesson, so find its ID
    const defaultExpandedId = computed(
      () => textbook.value?.lessons?.find((lesson) => !lesson.completed)?.id
    );

    return { tabs, ...toRefs(state), textbook, defaultExpandedId };
  },
});
</script>
