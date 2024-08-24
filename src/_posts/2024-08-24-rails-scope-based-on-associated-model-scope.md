---
layout: post
title:  Creating a Rails Model Scope Based on the Scope in a Related Model
date:   2024-08-24 08:55:00 -0700
category: til
tags: 
   - rails
   - scope
   - model
   - merge
context: rails
excerpt: "Use `#joins` and `#merge` together to avoid duplicating the logic of the related model's scope."
published: true
---

Suppose you have a Rails application with these models:

```ruby
class Recipe < ApplicationRecord
  has_many :recipe_ingredients, dependent: :destroy
  has_many :ingredients, through: :recipe_ingredients
end

class RecipeIngredients < ApplicationRecord
  belongs_to :recipe
  belongs_to :ingredient
end

class Ingredient < ApplicationRecord
  has_many :recipe_ingredients, dependent: :destroy
  has_many :recipes, through: :recipe_ingredients
  
  scope :refrigerated, -> { where(requires_refrigeration: true) }
end
```

You want to be able to pull a list of recipes which have at least one ingredient
which needs to be refrigerated. One way to do this is create a scope like this:

```ruby
class Recipe < ApplicationRecord
  has_many :recipe_ingredients, dependent: :destroy
  has_many :ingredients, through: :recipe_ingredients

  scope :with_refrigerated_ingredient, -> { joins(:ingredients).where(ingredients: { requires_refrigeration: true } ).distinct }
end
```

This works, but it requires `Recipe` to know how `Ingredient` represents
refrigerated vs unrefrigerated ingredients. Instead, we can reuse the
scope on `Ingredient` to define our new scope on `Recipe` using
`ActiveRecord::Relation#merge`:

```ruby
class Recipe < ApplicationRecord
  has_many :recipe_ingredients, dependent: :destroy
  has_many :ingredients, through: :recipe_ingredients
  
  scope :with_refrigerated_ingredient, -> { joins(:ingredients).merge(Ingredient.refrigerated).distinct }
end
```

When called with another `ActiveRecord::Relation`, `#merge` combines conditions
from both relations. Here, we're taking the condition from the
`Ingredient.refrigerated` relation and adding it to the relation we're
building in our new scope. Note that we need to add `joins(:ingredients)` so
the ingredients table is available in the query so the
`Ingredient.refrigerated` scope can filter on it.


