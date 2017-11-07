local factory = require 'factories.random_goal_factory'

local entityLayer = [[
*********************
*                   *
*                   *
*********   *********
        *   *
        *   *
        *   *
        *   *
        *   *
        *   *
        *   *
        *   *
        *   *
        *   *
        *   *
        * P *
        *****
]]

return factory.createLevelApi{
    mapName = 'my_map',
    entityLayer = entityLayer,
    episodeLengthSeconds = 60
}
