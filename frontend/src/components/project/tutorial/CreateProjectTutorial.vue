<template>
  <el-dialog
    :title="'Create Projects'"
    v-model="dialogVisible"
    v-on:update:visible="$emit('update:dialogVisible', $event)"
    @close="$emit('update:dialogVisible', false)"
    width="40%"
  >
    <div class="container">
      <div class="row">
          <br><br>
            <p class="text" style="text-align: justify">
              Create a project to start with. <br>
              You can choose between classifying sequences and extracting relationships. <br>
              (Currently only supports sequence classification.)
            </p>
      </div>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="() => $emit('update:dialogVisible', false)">
          Understand
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>

// the form when user create/edit a project
export default {
  name: "CreatePorjectTutorial",
  props: { dialogVisible: Boolean, existingInfo: Object },
  setup() {
  },
  data() {
    return {};
  },
  methods: {
  },
};
</script>

<style scoped></style>
