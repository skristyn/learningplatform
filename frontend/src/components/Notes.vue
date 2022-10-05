<template>
  <!-- TODO refactor this whole component -->
  <div class="container">
    <!-- notes display -->
    <div v-if="showInput" class="notes">
      <div v-if="notes.length" class="notes-list">
        <p v-for="(note, index) in notes" :key="index">{{ note }}</p>
      </div>
      <p v-else>Add notes for this lesson</p>
      <button @click="toggleInput">Add note</button>
    </div>

    <!-- notes input form -->
    <form v-else class="form" @submit.prevent="addNote">
      <ion-icon
        class="close-icon"
        name="close-circle-outline"
        @click="toggleInput"
      ></ion-icon>
      <textarea
        name="note"
        id="note"
        aria-label="Enter note here"
        placeholder="Enter note here"
        v-model="note"
      ></textarea>
      <button type="submit" :disabled="!note">Save</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { ref } from "vue";

export default defineComponent({
  name: "Notes",
  setup() {
    const note = ref<string>("");
    const notes = ref<string[]>([]);
    const showInput = ref(true);

    const toggleInput = () => {
      showInput.value = !showInput.value;
    };

    // TODO addNote should also send the notes[] update to the database
    const addNote = () => {
      if (note.value.trim() !== "") {
        notes.value.push(note.value);
      }
      note.value = "";

      toggleInput();
    };

    return { note, notes, showInput, addNote, toggleInput };
  },
});
</script>

<style scoped>
button {
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
}

.container {
  align-self: center;
  display: flex;
  flex-flow: column nowrap;
  align-items: flex-end;
}

.notes {
  display: flex;
  flex-flow: column nowrap;
  justify-content: space-between;
  border: 1px solid gray;
  padding: 5px;
  height: 150px;
  width: 300px;
}

.notes .notes-list {
  overflow-y: auto;
  margin-bottom: 5px;
}

.notes button {
  align-self: flex-end;
}

.form {
  display: flex;
  flex-flow: column nowrap;
  align-items: flex-end;
  margin-top: -14px;
}

.form textarea {
  resize: none;
  height: 150px;
  width: 300px;
}

.form button {
  margin: -29px 5px 0;
}

.form .close-icon {
  font-size: 30px;
  cursor: pointer;
  margin-right: -10px;
  margin-bottom: -16px;
  background: white;
}
</style>
