namespace BotAction.Role
{
	public class MechanicHero : BotActionBase
	{
		private float stopUseKnifeTime;

		public MechanicHero(Bot bot)
			: base(null)
		{
		}

		private void Bot_Getter_WeaponSlot(ref int slot, ref int priority)
		{
		}

		public override void Update()
		{
		}

		public override bool CanDo()
		{
			return false;
		}

		public override void DoAction()
		{
		}

		protected override void OnActionFinish()
		{
		}
	}
}
