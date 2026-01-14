generate-music
extend-music
upload-and-cover-audio
upload-and-extend-audio
add-instrumental
add-vocals
replace-section

```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
        "audio_id": "62e4542a-73be-44e1-b397-7716ee7505c6",
        "audio_url": "https://storage.vidgo.ai/audio/8FDN1I7M7Q68DDG8/20251125113627_QIivN2_tmphb8rgpeb_audio_62e4542a-73be-44e1-b397-7716ee7505c6.mp3",
        "image_url": "https://storage.vidgo.ai/audio/8FDN1I7M7Q68DDG8/20251125113628_4DfWp6_tmpz72j05o5_cover_62e4542a-73be-44e1-b397-7716ee7505c6.jpeg",
        "title": "Peaceful Piano Meditation",
        "tags": "Classical",
        "duration": 240,
         "prompt": ""
      },
      {
        "audio_id": "8e755734-a840-4c13-beac-b9f1044979ca",
        "audio_url": "https://storage.vidgo.ai/audio/8FDN1I7M7Q68DDG8/20251125113630_x7VTpV_tmpvsijwxa6_audio_8e755734-a840-4c13-beac-b9f1044979ca.mp3",
        "image_url": "https://storage.vidgo.ai/audio/8FDN1I7M7Q68DDG8/20251125113631_3MTe5V_tmp98wzcx2m_cover_8e755734-a840-4c13-beac-b9f1044979ca.jpeg",
        "title": "Peaceful Piano Meditation",
        "tags": "Classical",
        "duration": 130,
         "prompt": ""
      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```


get-timestamped-lyrics

```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
         "timestampe_lyrics" : "閼惧嘲褰囩敮锔芥闂傚瓨鍩戦惃鍕摃鐠?
      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```

boost-music-style

```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
         "style" : "閹绘劕宕岄棅鍏呯妞嬪孩鐗?
      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```

generate-music-cover

```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
         "image_url" : "閻㈢喐鍨氶棅鍏呯鐏忎線娼?
      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```

generate-persona

```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
         "persona_id" : "persona_id"
      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```

generate-lyrics
```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
       "title": "Peaceful Piano Meditation",  // Lyrics title
  "text": "Peaceful Piano Meditation", // Lyrics content, returns complete lyrics text on success

      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```

convert-to-wav

```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
       "wav_url": "",
      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```

separate-vocals

```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
       "vocal_removal": '{"vocal_url ": "xx", "instrumental_url" : "yy"}'
      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```

stem-split

```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
       "vocal_removal": '{"backing_vocals_url ": "", "bass_url " : "",  "brass_url " : "", "drums_url  " : "", "fx_url" : "", "guitar_url" : "", "keyboard_url" : "", "percussion_url" : "", "strings_url" : "", "synth_url" : "", "vocal_url" : "", "woodwinds_url" : "", "piano_url" : ""}'
      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```

upload-and-separate-vocals

```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
       "vocal_removal": '{"bass ": "", "drums" : "",  "piano" : "", "guitar" : "", "vocals" : "", "other" : ""}'
      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```

generate-midi
```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
         "midi_data" : '
     "state": "complete",
      "instruments": [
        {
          "name": "Drums",
          "notes": [
            {
              "pitch": 73,
              "start": 0.036458333333333336,
              "end": 0.18229166666666666,
              "velocity": 1
            },
            {
              "pitch": 61,
              "start": 0.046875,
              "end": 0.19270833333333334,
              "velocity": 1
            }
          ]
        },
        {
          "name": "Electric Bass (finger)",
          "notes": [
            {
              "pitch": 44,
              "start": 7.6875,
              "end": 7.911458333333333,
              "velocity": 1
            }
          ]
        }
      ]
'
      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```

create-music-video

```json
{
  "code": 200,
  "data": {
    "task_id": "8FDN1I7M7Q68DDG8",
    "status": "finished",
    "files": [
      {
       "video_url": " "
      }
    ],
    "created_time": "2025-11-25T08:50:13",
    "error_message": null
  }
}
```
