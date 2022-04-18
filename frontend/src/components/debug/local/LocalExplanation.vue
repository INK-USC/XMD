<template>
  <el-row style="width: 100%">
    <el-row style="width: 100%">
      <div
        style="
          display: flex;
          align-items: center;
          justify-content: space-between;
        "
      >
        <h1 style="text-align: center">
          Annotate page ({{ TaskTypes[this.projectStore.task] }})
        </h1>
        <!-- <div>
        <AnnotateHelp />
      </div> -->
      </div>
    </el-row>
    <el-row style="width: 100%">
      <el-progress
        style="width: 100%"
        :percentage="annotationCompletionPercentage"
        :format="getProgressBarLabel"
        type="line"
        :stroke-width="30"
        text-inside
      />
      <div style="width: 100%">
        <span class="demonstration" v-if="topK > 0">Top {{ topK }} words</span>
        <span class="demonstration" v-if="topK == 0">All words</span>
        <el-slider
          v-model="topK"
          :max="this.detailedDocumentStore.getMaxWords"
        />
      </div>
    </el-row>
    <el-card
      style="width: 100%; margin-top: 10px"
      v-if="this.detailedDocumentStore.getDocument"
    >
      <el-row>
        <el-col :span="16">
          <el-row>
            <el-tag>Words</el-tag>
          </el-row>
          <el-row style="line-height: 2; margin-top: 10px">
            <div>
              <span
                style="padding: 3px; font-size: 18px"
                v-for="wordData in this.detailedDocumentStore.getDocument.words"
                :key="wordData.id"
              >
                {{ wordData.text }}
              </span>
            </div>
          </el-row>
          <el-divider />
          <el-row>
            <el-tag>Annotations</el-tag>
          </el-row>
          <el-row
            style="margin-top: 10px"
            v-for="annotation in this.detailedDocumentStore.getDocument
              .annotations"
            :key="annotation.id"
          >
            <el-row style="width: 100%">
              <!-- TODO: Task based -->
              <el-tag>Label: {{ getLabelByID(annotation.label).text }}</el-tag>
              <div
                style="margin-left: 5px; padding: 5px; border: 2px solid black"
              >
                <span
                  v-for="(color, color_index) in this.getColors(
                    annotation.label
                  )"
                  :key="color_index"
                  :style="color"
                  style="margin-left: 5px; padding: 5px; font-size: 13px"
                >
                  Word
                </span>
              </div>
            </el-row>
            <el-row style="line-height: 2; margin-top: 10px">
              <div>
                <span
                  v-for="wordData in this.detailedDocumentStore.getDocument
                    .words"
                  :key="wordData.id"
                  :style="
                    getWordStyle(
                      wordData.scores[annotation.id],
                      annotation.label
                    )
                  "
                  @click="wordClick(annotation.id, wordData.id)"
                >
                  <el-popover
                    :content="
                      wordData.text +
                      ': ' +
                      wordData.scores[annotation.id].score
                    "
                    trigger="hover"
                  >
                    <template #reference>
                      <span>
                        {{ wordData.text }}
                      </span>
                    </template>
                  </el-popover>
                </span>
              </div>
            </el-row>
          </el-row>
        </el-col>
        <el-col :span="8">
          <el-table :data="dictTableData" border style="width: 100%">
            <!-- <el-table-column prop="word" label="Word" sortable /> -->
            <el-table-column label="Word">
              <template #default="scope">
                <span :style="getWordStyle(scope.row.score, scope.row.label)">
                  {{ scope.row.word }}
                </span>
              </template>
            </el-table-column>
            <el-table-column label="Operations">
              <template #default="scope">
                <el-popconfirm
                  title="Are you sure?"
                  @confirm="wordDelete(scope.row.id)"
                  style="margin-left: 10px"
                >
                  <template #reference>
                    <el-button size="small" type="danger"
                      ><el-icon><Delete /></el-icon>Delete</el-button
                    >
                  </template>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </el-card>

    <el-row style="margin-top: 20px; width: 100%">
      <el-col style="display: flex; justify-content: space-between">
        <el-button
          type="primary"
          @click="goToPrevDoc()"
          :disabled="
            this.documentStore.getdocumentInfo.curDocIndex === 0 &&
            this.documentStore.getdocumentInfo.curPage === 1
          "
        >
          <el-icon><ArrowLeft /></el-icon>
          Prev
        </el-button>
        <el-button
          type="primary"
          @click="goToNextDoc()"
          :disabled="
            this.documentStore.getdocumentInfo.curDocIndex ===
              this.documentStore.getdocumentInfo.documents.length - 1 &&
            this.documentStore.getdocumentInfo.curPage ===
              this.documentStore.getdocumentInfo.maxPage
          "
        >
          Next <el-icon><ArrowRight /></el-icon>
        </el-button>
      </el-col>
    </el-row>
    <el-row
      style="margin-top: 10px; width: 100%"
      v-if="this.detailedDocumentStore.getDocument"
    >
      <el-col style="display: flex; justify-content: flex-end">
        <el-button type="primary" @click="noAnnotation">
          Skip (Nothing to Mark Up)<el-icon><ArrowRight /></el-icon>
        </el-button>
      </el-col>
    </el-row>
  </el-row>
</template>

<script>
import { ArrowLeft, ArrowRight, Delete } from "@element-plus/icons-vue";

import { useDocumentStore } from "@/stores/document";
import { useDetailedDocumentStore } from "@/stores/detailedDocument";
import { useProjectStore } from "@/stores/project";
import { useLabelStore } from "@/stores/label";
import { useLocalDictionaryStore } from "@/stores/dictionaryLocal";
import { TaskTypes, ColorSets } from "@/utilities/constants";

export default {
  name: "LocalExplanations",
  components: {
    ArrowLeft,
    ArrowRight,
    Delete,
  },
  setup() {
    const documentStore = useDocumentStore();
    const detailedDocumentStore = useDetailedDocumentStore();
    const projectStore = useProjectStore();
    const localDictionaryStore = useLocalDictionaryStore();
    const labelStore = useLabelStore();
    return {
      documentStore,
      detailedDocumentStore,
      projectStore,
      localDictionaryStore,
      labelStore,
      TaskTypes,
      getLabelByID: labelStore.getLabelByID,
    };
  },
  data() {
    return {
      topK: 3,
    };
  },
  methods: {
    wordDelete(dictID) {
      this.localDictionaryStore.deleteWord(dictID);
    },
    wordClick(annID, wordID) {
      const docID = this.detailedDocumentStore.getDocument.id;
      const dictID = this.localDictionaryStore.fetchIfExists(
        docID,
        wordID,
        annID
      );
      if (dictID === null) {
        this.localDictionaryStore.addWord(docID, {
          word: wordID,
          annotation: annID,
        });
      }
      //  else {
      //   this.localDictionaryStore.deleteWord(dictID);
      // }
    },
    getColors(labelID) {
      const label = this.getLabelByID(labelID);
      return ColorSets[label.color_set].colors;
    },
    getWordStyle(scoreAnn, labelID) {
      const style = {
        padding: "3px 3px 3px 3px",
        margin: "3px 3px 3px 3px",
        fontSize: "18px",
      };
      if (this.topK > 0 && scoreAnn.order >= this.topK) {
        return style;
      }
      const score = scoreAnn.score;
      const colors = this.getColors(labelID);
      let index = -1;
      if (score <= 0) {
        return style;
      } else if (score <= 0.33) {
        index = 0;
      } else if (score <= 0.66) {
        index = 1;
      } else if (score <= 1.0) {
        index = 2;
      }
      return {
        ...style,
        ...colors[index],
      };
    },
    // get the string for progress bar
    getProgressBarLabel() {
      let documentInfo = this.documentStore.getdocumentInfo;
      return `${documentInfo.annotatedDocCount} / ${documentInfo.totalDocCount} documents annotated`;
    },
    // go to prev document
    goToPrevDoc() {
      const curDocIndex = this.documentStore.getdocumentInfo.curDocIndex - 1;
      if (curDocIndex == -1) {
        this.documentStore
          .updateCurPage(this.documentStore.getdocumentInfo.curPage - 1)
          .then(() => {
            this.documentStore.setCurDocIndex(
              this.documentStore.getDocuments.length - 1
            );
            this.detailedDocumentStore.fetchDocument(
              this.documentStore.getDocuments[
                this.documentStore.getDocuments.length - 1
              ].id
            );
          });
      } else {
        this.documentStore.setCurDocIndex(curDocIndex);
        this.detailedDocumentStore.fetchDocument(
          this.documentStore.getDocuments[curDocIndex].id
        );
      }
    },
    // go to next document
    goToNextDoc() {
      const curDocIndex = this.documentStore.getdocumentInfo.curDocIndex + 1;
      if (this.documentStore.getDocuments.length == curDocIndex) {
        this.documentStore
          .updateCurPage(this.documentStore.getdocumentInfo.curPage + 1)
          .then(() => {
            this.detailedDocumentStore.fetchDocument(
              this.documentStore.getDocuments[0].id
            );
            this.localDictionaryStore.fetchDictionary(
              this.documentStore.getDocuments[0].id
            );
          });
      } else {
        this.documentStore.setCurDocIndex(curDocIndex);
        this.detailedDocumentStore.fetchDocument(
          this.documentStore.getDocuments[curDocIndex].id
        );
        this.localDictionaryStore.fetchDictionary(
          this.documentStore.getDocuments[curDocIndex].id
        );
      }
    },
    noAnnotation() {
      this.documentStore.markAnnotated().then(() => {
        const curDocIndex = this.documentStore.getdocumentInfo.curDocIndex + 1;
        if (
          this.documentStore.getDocuments.length !== curDocIndex &&
          this.documentStore.getdocumentInfo.curPage !==
            this.documentStore.getdocumentInfo.maxPage
        ) {
          this.goToNextDoc();
        }
      });
    },
  },
  computed: {
    // get the percentage of the annotation progress
    annotationCompletionPercentage: function () {
      let documentInfo = this.documentStore.getdocumentInfo;
      if (documentInfo.totalDocCount == 0) {
        return 0;
      } else {
        let percentage =
          (100 * documentInfo.annotatedDocCount) / documentInfo.totalDocCount;
        return percentage;
      }
    },
    dictTableData: function () {
      const docID = this.detailedDocumentStore.getDocument.id;
      const words = this.localDictionaryStore.getByDocumentID(docID);
      const data = [];
      if (docID === undefined || words === undefined) return data;
      const allWords = this.detailedDocumentStore.getDocument.words;
      for (const wordData of allWords) {
        const wordID = wordData.id;
        if (!(wordID in words)) {
          continue;
        }
        const annotations = words[wordID];
        for (const annID in annotations) {
          const dictID = annotations[annID];
          const annScore = wordData.scores[annID].score;
          let label;
          for (const annData of this.detailedDocumentStore.getDocument
            .annotations) {
            if (annData.id == annID) {
              label = annData.label;
              break;
            }
          }
          data.push({
            id: dictID,
            word: wordData.text,
            score: {
              score: annScore,
              order: 0, // to override and display
            },
            label,
          });
        }
      }
      return data;
    },
  },
};
</script>
