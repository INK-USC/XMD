<template>
  <el-dialog
    v-model="dialogVisible"
    v-on:update:visible="$emit('update:dialogVisible', $event)"
    @close="$emit('update:dialogVisible', false)"
    width="50%"
  >
    <span slot="title" style="font-size: 18pt; font-weight:bold">XMD Workflow</span>
    <div class="container">
      <div class="row" style="padding: 10px">
          <br><br>
            <p class="text" style="font-size: 15pt; text-align: justify">
              1. Upload your train data. <br>
              2. Load your trained model. <br>
              3. Generate explanations on your train data using the trained model. <br>
              4. Select words to increase or decrease its importance score. <br>
              5. Start debug the model. <br>
              6. Download the debugged model and see how explanation is changed. <br>
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
  name: "WorkflowTutorial",
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
