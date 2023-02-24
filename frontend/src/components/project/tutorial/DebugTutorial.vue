<template>
  <el-dialog
    v-model="dialogVisible"
    v-on:update:visible="$emit('update:dialogVisible', $event)"
    @close="$emit('update:dialogVisible', false)"
    width="50%"
  >
    <span slot="title" style="font-size: 18pt; font-weight:bold">Model Debugging</span>
    <div class="container">
      <div class="row" style="padding: 10px">
          <br><br>
            <p class="text" style="font-size: 15pt; text-align: justify">
              You will debug the model by selecting words to increase or decrease its importance score. <br>
              You can select words for each instance (Instance Explanation) or words that apply to all instances (Task Explanation). <br>
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
  name: "DebugTutorial",
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
