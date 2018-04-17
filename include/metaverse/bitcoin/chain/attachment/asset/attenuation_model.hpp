/**
 * Copyright (c) 2016-2018 metaverse core developers (see MVS-AUTHORS)
 *
 * This file is part of mvs-node.
 *
 * metaverse is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License with
 * additional permissions to the one published by the Free Software
 * Foundation, either version 3 of the License, or (at your option)
 * any later version. For more information see LICENSE.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef MVS_CHAIN_ATTACHMENT_ASSET_ATTENUATION_MODEL_HPP
#define MVS_CHAIN_ATTACHMENT_ASSET_ATTENUATION_MODEL_HPP

#include <cstdint>
#include <metaverse/bitcoin/chain/point.hpp>
#include <metaverse/bitcoin/chain/script/script.hpp>
#include <metaverse/bitcoin/define.hpp>

using namespace libbitcoin::chain;

#define MODEL2UINT8(model)  (static_cast<typename std::underlying_type<attenuation_model::model_index>::type>(model))
#define ATTENUATION_MODEL_NONE              MODEL2UINT8(attenuation_model::model_index::none)
#define ATTENUATION_MODEL_FIXED_QUANTITY    MODEL2UINT8(attenuation_model::model_index::fixed_quantity)
#define ATTENUATION_MODEL_FIXED_RATE        MODEL2UINT8(attenuation_model::model_index::fixed_rate)
#define ATTENUATION_MODEL_FIRST_UNUSED      MODEL2UINT8(attenuation_model::model_index::unused1)


namespace libbitcoin {
namespace chain {
// forward declaration
class asset_detail;

class attenuation_model
{
public:
    enum model_index : uint8_t
    {
        none = 0,
        fixed_quantity = 1,
        fixed_rate = 2,
        unused1 = 3,
        unused2 = 4,
        unused3 = 5,
        unused4 = 6,
        unused5 = 7,
        invalid = 8
    };

    static bool check_model_index(uint32_t index);
    static bool check_model_param(uint32_t index, const data_chunk& param);

private:
    model_index model_index_{model_index::none};
};

} // namespace chain
} // namespace libbitcoin

#endif

