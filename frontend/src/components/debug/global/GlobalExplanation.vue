<template>
  <el-row style="width: 100%">
    <el-row style="width: 100%">
      <div style=" display: flex; align-items: center; justify-content: space-between;">
        <h1 style="text-align: center">
          Annotate page (Task Explanation)
          <el-popover content="Attribution scores refer to how much the word positively correlates to the ground truth label." trigger="hover" :width="400">
            <template #reference>
              <el-icon style="height: 100%; margin-left: 0.5rem">
                <QuestionFilled />
              </el-icon>
            </template>
          </el-popover>
        </h1>
        <!-- <div>
          <AnnotateHelp />
        </div> -->
      </div>
    </el-row>

    <el-row
      style="margin-top: 20px; width: 100%"
      v-if="wordStore.getCurrWord() !== undefined"
    >
      <el-col style="display: flex; justify-content: space-between">
        <el-button
          type="primary"
          @click="goToPrevWord()"
          :disabled="
            this.wordStore.getWordInfo.curWordIndex === 0 &&
            this.wordStore.getWordInfo.curPage === 1"
        >
          <el-icon><ArrowLeft /></el-icon>
          Prev
        </el-button>
        <el-button
          type="primary"
          @click="goToNextWord()"
          :disabled="
            this.wordStore.getWordInfo.curWordIndex === this.wordStore.getWordInfo.words.length - 1 && 
            this.wordStore.getWordInfo.curPage === this.wordStore.getWordInfo.maxPage"
        >
          Next <el-icon><ArrowRight /></el-icon>
        </el-button>
      </el-col>
    </el-row>

    <el-card style="width: 100%; margin-top: 10px" v-if="wordStore.wordLoaded">
      <template #header>
        <div>
          Current Word: <b>{{ this.wordStore.getCurrWord() }} </b>

          <div style="margin-left: 10px; display: inline-block">
            <el-button
              size="small"
              type="success"
              @click="addWord(0)"
              v-if="!globalDictionaryStore.containsWord(wordStore.getCurrWord())"
              >
              add
            </el-button>
            <el-button
              size="small"
              type="primary"
              @click="addWord(1)"
              v-if="!globalDictionaryStore.containsWord(wordStore.getCurrWord())"
            >
              remove
            </el-button>
            <el-button
              size="small"
              type="info"
              @click="globalDictionaryStore.deleteWord(wordStore.getCurrWord())"
              v-if="globalDictionaryStore.containsWord(wordStore.getCurrWord())"
            >
              reset
            </el-button>
            <el-popover content="If you think positively correlated words (red-colored) should not be correlated to the ground truth label prediction, delete those words! If you think weakly correlated words should be correlated to the ground truth label, add those words!" trigger="hover" :width="400">
                <template #reference>
                  <el-icon style="height: 100%; margin-left: 0.5rem">
                    <QuestionFilled />
                  </el-icon>
                </template>
              </el-popover>
          </div>
        </div>
      </template>
      <el-row
        style="width: 100%"
        v-for="(document, docIndex) in documents"
        :key="document.id"
      >
        <!-- <el-row style="width: 100%; margin-bottom: 5px">
          <el-tag>Document #{{ docIndex + 1 }}</el-tag>
          <el-tag style="margin-left: 10px" v-if="'ground_truth' in document">
            Ground truth: {{ getLabelByID(document.ground_truth).text }}
          </el-tag>
        </el-row> -->
        <el-row
          style="width: 100%"
          v-for="annotation in document.annotations"
          :key="annotation.id"
        >
          <el-row style="width: 100%">
            <!-- TODO: Task based -->
            <el-tag>Document #{{ docIndex + 1 }}</el-tag>
            <el-tag style="margin-left: 10px" v-if="'ground_truth' in document">
              Ground truth: {{ getLabelByID(document.ground_truth).text }}
            </el-tag>
            <el-tag style="margin-left: 10px">
              Prediction: {{ getLabelByID(annotation.label).text }}
            </el-tag>
            <!-- <div
              style="margin-left: 5px; padding: 5px; border: 2px solid black"
            >
              <span
                v-for="(color, color_index) in this.getColors(annotation.label)"
                :key="color_index"
                :style="color"
                style="margin-left: 5px; padding: 5px; font-size: 13px"
              >
                Word
              </span>
            </div> -->
          </el-row>
          <el-row style="line-height: 2; margin-top: 10px">
            <div>
              <span
                v-for="wordData in document.words"
                :key="wordData.id"
                :style="getWordStyle(wordData.scores[annotation.id], annotation.label)"
              >
                <el-popover
                  :content=" wordData.text + ': ' + wordData.scores[annotation.id].score "
                  trigger="hover"
                >
                  <template #reference>
                    <span
                      :style="
                        wordData.text === this.wordStore.getCurrWord() ? { border: '2px solid black' } : {}"
                    >
                      {{ wordData.text }}
                    </span>
                  </template>
                </el-popover>
              </span>
            </div>
          </el-row>
        </el-row>
        <el-divider />
      </el-row>
    </el-card>
  </el-row>
  <GlobalDebugTutorial
    v-model:dialog-visible="tutorialVisible"
  />
</template>

<script>
import { QuestionFilled} from "@element-plus/icons-vue";
import { ArrowLeft, ArrowRight } from "@element-plus/icons-vue";

import { useWordStore } from "@/stores/word";
import { useProjectStore } from "@/stores/project";
import { useLabelStore } from "@/stores/label";
import { useGlobalDictionaryStore } from "@/stores/dictionaryGlobal";
import { TaskTypes, ColorSets } from "@/utilities/constants";
import GlobalDebugTutorial from "@/components/project/tutorial/GlobalDebugTutorial.vue";

export default {
  name: "GlobalExplanations",
  components: {
    ArrowLeft,
    ArrowRight,
    QuestionFilled,
    GlobalDebugTutorial,
  },
  setup() {
    const labelStore = useLabelStore();
    const wordStore = useWordStore();
    const globalDictionaryStore = useGlobalDictionaryStore();
    const projectStore = useProjectStore();
    return {
      labelStore,
      wordStore,
      globalDictionaryStore,
      projectStore,
      TaskTypes,
      getLabelByID: labelStore.getLabelByID,
    };
  },
  data() {
    return {
      tutorialVisible: true,
    };
  },
  computed: {
    documents: function () {
      return this.wordStore.getDocuments;
    },
  },
  methods: {
    addWord(type) {
      this.globalDictionaryStore.addWord(
        this.wordStore.getCurrWord(),
        type,
        this.getLabelByID(this.documents[0].ground_truth).id
      );
    },
    getWordStyle(scoreAnn, labelID) {
      const style = {
        padding: "3px 3px 3px 3px",
        margin: "3px 3px 3px 3px",
        fontSize: "18px",
      };
      const score = scoreAnn.score;
      const colors = ColorSets[1].colors;
      let index = -1;
      if (score <= 0.1) {
        return style;
      } else if (score <= 0.5) {
          index = 0;
      } else if (score <= 0.75) {
          index = 1;
      } else if (score <= 1) {
          index = 2;
      }
      return {
          ...style,
          ...colors[index],
      };
    },
    // go to prev word
    goToPrevWord() {
      const curWordIndex = this.wordStore.getWordInfo.curWordIndex - 1;
      if (curWordIndex == -1) {
        this.wordStore
          .updateCurPage(this.wordStore.getWordInfo.curPage - 1)
          .then(() => {
            this.wordStore.setCurWordIndex(this.wordStore.getWords.length - 1);
            this.wordStore.fetchDocuments();
          });
      } else {
        this.wordStore.setCurWordIndex(curWordIndex);
        this.wordStore.fetchDocuments();
      }
    },
    // go to next word
    goToNextWord() {
      const curWordIndex = this.wordStore.getWordInfo.curWordIndex + 1;
      if (this.wordStore.getWords.length == curWordIndex) {
        this.wordStore
          .updateCurPage(this.wordStore.getWordInfo.curPage + 1)
          .then(() => {
            this.wordStore.fetchDocuments();
          });
      } else {
        this.wordStore.setCurWordIndex(curWordIndex);
        this.wordStore.fetchDocuments();
      }
    },
  },
};
</script>
