namespace BotAction.Skill
{
	public class DistanceUse : BotSkillBase
	{
		private float minDis;

		private float maxDis;

		public DistanceUse(Bot bot, SkillKey skillKey, float minDistance, float maxDistance)
			: base(null, SkillKey.F)
		{
		}

		public override bool CanDo()
		{
			return false;
		}
	}
}
