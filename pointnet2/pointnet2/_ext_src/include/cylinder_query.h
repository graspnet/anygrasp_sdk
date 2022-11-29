// Copyright (c) Facebook, Inc. and its affiliates.
// 
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

#pragma once
#include <torch/extension.h>

at::Tensor cylinder_query(at::Tensor new_xyz, at::Tensor xyz, at::Tensor rot, const float radius, const float hmin, const float hmax,
                      const int nsample);
