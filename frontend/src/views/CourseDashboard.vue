<template>
  <PageHeader pageTitle="Digital Steward Training" />
  <!-- when Tabs emits the onSelectedTab event, take its tabTitle and set selectedTab state to this string value -->
  <Tabs
    :tabs="tabs"
    :selectedTab="selectedTab"
    @onSelectTab="selectedTab = $event"
  />
  <div v-if="selectedTab === 'Lessons'">
    <p>lessons placeholder</p>
  </div>
  <div v-if="selectedTab === 'Resources'">
    <p>resources placeholder</p>
  </div>
  <div v-if="selectedTab === 'Project'">
    <p>project placeholder</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs } from "vue";
import PageHeader from "@/components/PageHeader.vue"; // @ is an alias to /src
import Tabs from "@/components/Tabs.vue";

export default defineComponent({
  name: "CourseDashboard",
  components: {
    PageHeader,
    Tabs,
  },
  setup() {
    const tabs = [
      { ionIconName: "book-outline", tabTitle: "Lessons" },
      { ionIconName: "briefcase-outline", tabTitle: "Resources" },
      { ionIconName: "clipboard-outline", tabTitle: "Project" },
    ];

    const state = reactive({
      selectedTab: "Lessons",
    });

    return { tabs, ...toRefs(state) };
  },
});
</script>
