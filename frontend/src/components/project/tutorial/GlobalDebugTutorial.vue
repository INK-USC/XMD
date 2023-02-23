<template>
  <el-dialog
    :title="'Task Explanation'"
    v-model="dialogVisible"
    v-on:update:visible="$emit('update:dialogVisible', $event)"
    @close="$emit('update:dialogVisible', false)"
    width="40%"
  >
    <div class="container">
      <div class="row">
          <br><br>
            <p class="text" style="text-align: justify">
              Select words to debug for all instances. <br>
              Attribution scores refer to how much the word positively correlates to the ground truth label. <br>
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
  name: "GlobalDebugTutorial",
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
