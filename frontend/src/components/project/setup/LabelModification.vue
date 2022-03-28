<template>
  <el-row style="width: 100%">
    <el-card style="width: 100%">
      <template #header><h3>Label Space Creation</h3></template>
      <div style="text-align: left">
        <el-row>
          <el-col :span="8">
            <el-popover
              content="Available labels for model to predict."
              trigger="hover"
            >
              <template #reference>
                <span>
                  <b>Current Label Space</b>
                  <el-icon style="margin-left: 5px">
                    <QuestionFilled />
                  </el-icon>
                </span>
              </template>
            </el-popover>
          </el-col>
        </el-row>

        <el-divider />
        <el-form :model="colors_sets">
          <el-row v-for="(label, index) in this.existingLabels" :key="label.id">
            <el-form-item :label="label.text">
              <el-select
                v-model="this.colors_sets[index]"
                placeholder="Select"
                style="width: 100%"
              >
                <el-option
                  v-for="item in this.colorSetOptions"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
            <div style="margin-left: 5px">
              <span
                v-for="(color, color_index) in this.getColors(
                  this.colors_sets[index]
                )"
                :key="color_index"
                :style="color"
                style="margin-left: 5px; padding: 5px"
              >
                Word
              </span>
            </div>
          </el-row>

          <el-row>
            <el-button
              type="success"
              :disabled="this.disableButton"
              @click="goNextStep"
            >
              Done
            </el-button>
          </el-row>
        </el-form>
      </div>
    </el-card>
  </el-row>
</template>

<script>
import { QuestionFilled } from "@element-plus/icons-vue";
import { useLabelStore } from "@/stores/label";
import { ColorSets } from "@/utilities/constants";

// create label.
export default {
  name: "LabelModificationPage",
  components: { QuestionFilled },
  setup() {
    const labelStore = useLabelStore();
    const colorSetOptions = [];
    for (let item in ColorSets) {
      colorSetOptions.push({
        id: item,
        name: ColorSets[item].name,
      });
    }
    return {
      labelStore,
      colorSetOptions,
    };
  },
  data() {
    return {
      existingLabels: [],
      colors_sets: [],
      saving: false,
    };
  },
  methods: {
    goNextStep() {
      this.saving = true;
      console.log(this.colors_sets);
      const promises = [];
      for (let index = 0; index < this.existingLabels.length; index++) {
        const label = this.existingLabels[index];
        const color_set = parseInt(this.colors_sets[index]);
        if (label.color_set != color_set) {
          label.color_set = color_set;
          promises.push(this.labelStore.updateLabel(label));
        }
      }
      Promise.all(promises).then(() => {
        this.saving = false;
        this.labelStore.fetchLabels();
        this.$router.push({ name: "GenerateExplanations" });
      });
    },
    getColors(color_set) {
      color_set = parseInt(color_set);
      if (color_set in ColorSets) {
        return ColorSets[color_set].colors;
      }
      return [];
    },
  },
  created() {
    this.labelStore.fetchLabels().then((res) => {
      const colors_sets = {};
      for (let label in res) {
        colors_sets[label] = "" + res[label].color_set;
      }
      this.colors_sets = colors_sets;
      this.existingLabels = res;
    });
  },
  computed: {
    disableButton() {
      if (this.saving) return true;
      // if (this.labelStore.getLabels === this.existingLabels) return true;
      const visited = {};
      for (let item in this.colors_sets) {
        if (item in visited) {
          return true;
        }
        visited[item] = null;
      }
      return false;
    },
  },
};
</script>
