<template>
  <h3>Debug Overview Page</h3>

  <el-button
        type="primary"
        @click="trainDebugModel()">
        Start Debug Training
  </el-button> <br />

  <el-row style="width: 100%; margin-top: 3em;">
    Instance Explanation
    <el-progress
        style="width: 100%; margin-top: 1em;"
        :percentage="instanceAnnotationCompletionPercentage"
        :format="getInstanceProgressBarLabel"
        type="line"
        :stroke-width="30"
        text-inside
      />
  </el-row>
  <el-row style="width: 100%; margin-top: 3em;">
    Task Explanation
    <el-progress
        style="width: 100%; margin-top: 1em;"
        :percentage="instanceAnnotationCompletionPercentage"
        :format="getInstanceProgressBarLabel"
        type="line"
        :stroke-width="30"
        text-inside
      />
  </el-row>
</template>


<script>
import { useProjectStore } from "@/stores/project";
import { useDocumentStore } from "@/stores/document";
import { useGlobalDictionaryStore } from "@/stores/dictionaryGlobal";
import { useWordStore } from "@/stores/word";
import DebugTrainingAPI from "@/utilities/network/debugTraining"
import DocumentsApi from "@/utilities/network/document";

export default {
  name: "DebugOverview",
  setup() {
    const projectStore = useProjectStore();
    const documentStore = useDocumentStore();
    const globalDictionaryStore = useGlobalDictionaryStore();
    const wordStore = useWordStore();
    return {
      projectStore,
      documentStore,
      globalDictionaryStore,
      wordStore,
    };
  },
  methods: {
    // get the string for progress bar
    getInstanceProgressBarLabel() {
      let documentInfo = this.documentStore.getdocumentInfo;
      return `${documentInfo.annotatedDocCount} / ${documentInfo.totalDocCount} documents annotated`;
    },
    getTaskProgressBarLabel() {
      this.globalDictionaryStore.fetchDictionary();
      // this.wordStore.fetchDocuments();
      return `${this.globalDictionaryStore.getRows.length} / ${this.wordStore.getWordInfo.totalWordCount} documents annotated`;
    },
    fetchDebugScores(docID) {
      return DocumentsApi.detailedDocument(
        this.projectStore.getProjectInfo.id,
        docID
      ).then((res) => {
        console.log(res);
        console.log(res.words);
        for (let word of res.words) {
          console.log("word:", word.text);
          console.log("initial score:", word.word_annotation_score[0].score);
        //   // console.log("word:", word.text, "debug score:", word.word_debug_annotation_score.score)
        }
      })
    },
    trainDebugModel() {
      DebugTrainingAPI.train(this.projectStore.getProjectInfo.id);
      this.fetchDebugScores(this.documentStore.getDocuments[1].id)

      // waitForCompletion()
    },
    // waitForCompletion() {

    // },
  },
  computed: {
    // get the percentage of the annotation progress
    instanceAnnotationCompletionPercentage() {
      let documentInfo = this.documentStore.getdocumentInfo;
      if (documentInfo.totalDocCount == 0) {
        return 0;
      } else {
        let percentage =
          (100 * documentInfo.annotatedDocCount) / documentInfo.totalDocCount;
        return percentage;
      }
    },
    taskAnnotationCompletionPercentage() {
      this.globalDictionaryStore.fetchDictionary();
      let wordInfo = this.wordStore.getWordInfo;
      if (wordInfo.totalWordCount == 0) {
        return 0;
      } else {
        let percentage =
          (100 * this.globalDictionaryStore.getRows.length) / wordInfo.totalWordCount;
        return percentage;
      }
    }
  }
};
</script>
