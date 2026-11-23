using UnityEngine;

namespace BotAction
{
	public class BA_PickUpUpgradeBox : BotActionBase
	{
		private SupplyBox target;

		private bool ignoreBoxSavior;

		public BA_PickUpUpgradeBox(Bot bot)
			: base(null)
		{
		}

		private void Bot_Destination_Listener(ref Vector3 pos, ref int priority)
		{
		}

		public override bool CanDo()
		{
			return false;
		}

		public override void DoAction()
		{
		}

		private void FindUpgradeBox()
		{
		}
	}
}
