#!/usr/bin/env bash
set -e

# Usage:
# ./create-company.sh "NexusAI" "IT Software Company" "cloud, DevOps, AI agents, SaaS"

COMPANY_NAME="$1"
COMPANY_TYPE="$2"
COMPANY_FOCUS="$3"

if [ -z "$COMPANY_NAME" ] || [ -z "$COMPANY_TYPE" ] || [ -z "$COMPANY_FOCUS" ]; then
  echo "Usage: create-company.sh \"Company Name\" \"Company Type\" \"Company Focus\""
  exit 1
fi

BASE_DIR="$HOME/ai-holding"
TEMPLATE_DIR="$BASE_DIR/templates/company"

SLUG=$(echo "$COMPANY_NAME" \
  | tr '[:upper:]' '[:lower:]' \
  | sed 's/[^a-z0-9]/-/g' \
  | sed 's/-\+/-/g' \
  | sed 's/^-//' \
  | sed 's/-$//')

TARGET_DIR="$BASE_DIR/companies/$SLUG"

if [ -d "$TARGET_DIR" ]; then
  echo "Company already exists: $TARGET_DIR"
  exit 1
fi

cp -r "$TEMPLATE_DIR" "$TARGET_DIR"

find "$TARGET_DIR" -type f -name "*.md" -print0 | while IFS= read -r -d '' file; do
  sed -i "s/{{COMPANY_NAME}}/$COMPANY_NAME/g" "$file"
  sed -i "s/{{COMPANY_TYPE}}/$COMPANY_TYPE/g" "$file"
  sed -i "s/{{COMPANY_FOCUS}}/$COMPANY_FOCUS/g" "$file"
done

cat >> "$BASE_DIR/tasks/company-index.jsonl" <<EOF
{"name":"$COMPANY_NAME","slug":"$SLUG","type":"$COMPANY_TYPE","focus":"$COMPANY_FOCUS","path":"$TARGET_DIR","status":"ACTIVE"}
EOF

echo "Company created successfully."
echo "Name : $COMPANY_NAME"
echo "Slug : $SLUG"
echo "Path : $TARGET_DIR"
