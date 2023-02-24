<template>
  <el-dialog
    v-model="dialogVisible"
    v-on:update:visible="$emit('update:dialogVisible', $event)"
    @close="$emit('update:dialogVisible', false)"
    width="50%"
  >
    <span slot="title" style="font-size: 18pt; font-weight:bold">Explanation Generation</span>
    <div class="container">
      <div class="row" style="padding: 10px">
          <br><br>
            <p class="text" style="font-size: 15pt; text-align: justify">
              Load the model trained on the train data from local or huggingface modelhub. <br>
              Use that model to generate explanations for the train data. <br>
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
  name: "GenerateExplanationTutorial",
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
