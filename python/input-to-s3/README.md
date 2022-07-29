# Input to AWS S3
- [Input to AWS S3](#input-to-aws-s3)
  - [Usage](#usage)



## Usage

```bash
yarn build:refapps # build sequence
si sequence deploy dist/
si instance output -
```

On second terminal:
```bash
echo "Test" |si instance stdin <id>
```
